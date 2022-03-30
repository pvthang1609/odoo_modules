==============
Custom column width
==============

You can resize width table column and memory width table column

Usage
=====

* we input attrs width_column in <tree> tag
* If had attrs width_column table will resize else it not
* Example: <tree width_column='{"checkbox":40,"name":100,"company_name":200,"email":250,"lang":300}'>

.. image:: custom_column_width\static\description\width_table_2.png
    :width: 500

* New feature sticky column

.. image:: custom_column_width\static\description\sticky.png
    :width: 500

* Note: number of columns "displayed" corresponding to the number of items in attrs
* Note: if number of columns "displayed" corresponding to the number of items in attrs, remember width column active

.. image:: custom_column_width\static\description\width_table.png
    :width: 1000

* Result: they will had result in client (under image)

.. image:: custom_column_width\static\description\width_table_1.png
    :width: 1000

Author: `VNSolutions <https://vnsolution.com.vn>`_