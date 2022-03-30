import collections
import logging
import os

from lxml import etree
from odoo import api, models, tools, _
from odoo.exceptions import ValidationError
from odoo.tools.view_validation import valid_view, validate, _relaxng_cache

_logger = logging.getLogger(__name__)

MOVABLE_BRANDING = ['data-oe-model', 'data-oe-id', 'data-oe-field', 'data-oe-xpath', 'data-oe-source-id']

_validators = collections.defaultdict(list)


def tree_valid_view(arch, **kwargs):
    check = schema_valid(arch, **kwargs)
    if not check:
        _logger.error("Invalid XML: %s", schema_valid.__doc__)
        return False
    if check == "Warning":
        _logger.warning("Invalid XML: %s", schema_valid.__doc__)
        return "Warning"
    return True


@validate('calendar', 'graph', 'pivot', 'search', 'tree', 'activity')
def schema_valid(arch, **kwargs):
    """ Get RNG validator and validate RNG file."""
    validator = tree_relaxng(arch.tag)
    if validator and not validator.validate(arch):
        result = True
        for error in validator.error_log:
            _logger.error(tools.ustr(error))
            result = False
        return result
    return True


def tree_relaxng(view_type):
    """ Return a validator for the given view type, or None. """
    if view_type not in _relaxng_cache:
        with tools.file_open(os.path.join('custom_column_width', 'rng', '%s_view.rng' % view_type)) as frng:
            try:
                relaxng_doc = etree.parse(frng)
                _relaxng_cache[view_type] = etree.RelaxNG(relaxng_doc)
            except Exception:
                _logger.exception('Failed to load RelaxNG XML schema for views validation')
                _relaxng_cache[view_type] = None
    return _relaxng_cache[view_type]


class View(models.Model):
    _inherit = 'ir.ui.view'

    @api.constrains('arch_db')
    def _check_xml(self):
        # Sanity checks: the view should not break anything upon rendering!
        # Any exception raised below will cause a transaction rollback.
        partial_validation = self.env.context.get('ir_ui_view_partial_validation')
        self = self.with_context(validate_view_ids=(self._ids if partial_validation else True))

        for view in self:
            try:
                # verify the view is valid xml and that the inheritance resolves
                if view.inherit_id:
                    view_arch = etree.fromstring(view.arch)
                    view._valid_inheritance(view_arch)
                combined_arch = view._get_combined_arch()
                if view.type == 'qweb':
                    continue
            except ValueError as e:
                err = ValidationError(_(
                    "Error while validating view:\n\n%(error)s",
                    error=tools.ustr(e),
                )).with_traceback(e.__traceback__)
                err.context = getattr(e, 'context', None)
                raise err from None

            try:
                # verify that all fields used are valid, etc.
                view._validate_view(combined_arch, view.model)
                combined_archs = [combined_arch]
                if combined_archs[0].tag == 'data':
                    # A <data> element is a wrapper for multiple root nodes
                    combined_archs = combined_archs[0]
                for view_arch in combined_archs:
                    for node in view_arch.xpath('//*[@__validate__]'):
                        del node.attrib['__validate__']
                    if view_arch.tag == 'tree':
                        check = tree_valid_view(view_arch, env=self.env, model=view.model)
                    else:
                        check = valid_view(view_arch, env=self.env, model=view.model)
                    if not check:
                        view_name = ('%s (%s)' % (view.name, view.xml_id)) if view.xml_id else view.name
                        raise ValidationError(_(
                            'Invalid view %(name)s definition in %(file)s',
                            name=view_name, file=view.arch_fs
                        ))
                    if check == "Warning":
                        view_name = ('%s (%s)' % (view.name, view.xml_id)) if view.xml_id else view.name
                        _logger.warning('Invalid view %s definition in %s \n%s', view_name, view.arch_fs, view.arch)
            except ValueError as e:
                lines = etree.tostring(combined_arch, encoding='unicode').splitlines(keepends=True)
                fivelines = "".join(lines[max(0, e.context["line"] - 3):e.context["line"] + 2])
                err = ValidationError(_(
                    "Error while validating view near:\n\n%(fivelines)s\n%(error)s",
                    fivelines=fivelines, error=tools.ustr(e),
                ))
                err.context = e.context
                raise err.with_traceback(e.__traceback__) from None

        return True
