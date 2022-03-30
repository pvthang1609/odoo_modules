/** @odoo-module alias=inherit.EditableListRenderer **/

import ListRenderer from "web.ListRenderer";

ListRenderer.include({
  _freezeColumnWidths: function () {
    if (!this.columnWidths && this.el.offsetParent === null) {
      // there is no record nor widths to restore or the list is not visible
      // -> don't force column's widths w.r.t. their label
      return;
    }
    const thElements = [...this.el.querySelectorAll("table thead th")];
    if (!thElements.length) {
      return;
    }
    const table = this.el.getElementsByClassName("o_list_table")[0];
    let columnWidths = this.columnWidths;

    if (!columnWidths || !columnWidths.length) {
      // no column widths to restore
      // Set table layout auto and remove inline style to make sure that css
      // rules apply (e.g. fixed width of record selector)
      table.style.tableLayout = "auto";
      thElements.forEach((th) => {
        th.style.width = null;
        th.style.maxWidth = null;
      });

      // Resets the default widths computation now that the table is visible.
      this._computeDefaultWidths();

      // Squeeze the table by applying a max-width on largest columns to
      // ensure that it doesn't overflow
      const attrColumnWidth = this.arch.attrs.width_column;
      const obj = attrColumnWidth ? JSON.parse(attrColumnWidth) : false;
      const defaultColumnWidths = this._squeezeTable();
      const fieldName = [...table.getElementsByTagName("th")].map((i) => {
        const attr = i.getAttribute("data-name");
        if (attr) {
          return attr;
        } else {
          if (i.getAttribute("class") == "o_list_record_selector") {
            return "checkbox";
          } else {
            return "unknow";
          }
        }
      });
      const sizeColTable = JSON.parse(localStorage.getItem("sizeColTable") || "[]");
      const model = this.state.model;

      const staticColumnWidth = fieldName.reduce((acc, curValue) => {
        const size_col = sizeColTable.find(
          (i) => i.model === model && i.hasOwnProperty(curValue)
        );
        if (size_col) {
          return [...acc, size_col[curValue]];
        }
        else if (obj[curValue]) {
          return [...acc, obj[curValue]];
        } else {
          return acc;
        }
      }, []);

      const applyDefaultColumnWidth = fieldName.map((i,inx) => {
        const r = sizeColTable.find((s) => s.model === model && s.hasOwnProperty(i))
        if(r) {
          return r[i]
        } else {
          return defaultColumnWidths[inx]
        }
      })
      // Hàm _squeezeTable sẽ tự động điều chỉnh width
      // Ở đây trường hợp nếu có attrs width_column thì width của mỗi cột sẽ ở dưới dạng tĩnh
      if (
        attrColumnWidth &&
        staticColumnWidth.length === defaultColumnWidths.length
      ) {
        columnWidths = staticColumnWidth;
      } else {
        columnWidths = applyDefaultColumnWidth;
      }
    }

    thElements.forEach((th, index) => {
      // Width already set by default relative width computation
      if (!th.style.width) {
        th.style.width = `${columnWidths[index]}px`;
      }
    });

    // Set the table layout to fixed
    table.style.tableLayout = "fixed";
  },
  _onStartResize: function (ev) {
    // Only triggered by left mouse button
    if (ev.which !== 1) {
      return;
    }
    ev.preventDefault();
    ev.stopPropagation();

    this.isResizing = true;

    const table = this.el.getElementsByClassName("o_list_table")[0];
    const th = ev.target.closest("th");
    table.style.width = `${table.offsetWidth}px`;
    const thPosition = [...th.parentNode.children].indexOf(th);
    const resizingColumnElements = [...table.getElementsByTagName("tr")]
      .filter((tr) => tr.children.length === th.parentNode.children.length)
      .map((tr) => tr.children[thPosition]);
    const optionalDropdown =
      this.el.getElementsByClassName("o_optional_columns")[0];
    const initialX = ev.pageX;
    const initialWidth = th.offsetWidth;
    const initialTableWidth = table.offsetWidth;
    const initialDropdownX = optionalDropdown
      ? optionalDropdown.offsetLeft
      : null;
    const resizeStoppingEvents = ["keydown", "mousedown", "mouseup"];

    // Fix container width to prevent the table from overflowing when being resized
    if (!this.el.style.width) {
      this.el.style.width = `${this.el.offsetWidth}px`;
    }

    // Apply classes to table and selected column
    table.classList.add("o_resizing");
    resizingColumnElements.forEach((el) =>
      el.classList.add("o_column_resizing")
    );

    // Mousemove event : resize header
    const resizeHeader = (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      const delta = ev.pageX - initialX;
      const newWidth = Math.max(10, initialWidth + delta);
      const tableDelta = newWidth - initialWidth;
      th.style.width = `${newWidth}px`;
      th.style.maxWidth = `${newWidth}px`;
      table.style.width = `${initialTableWidth + tableDelta}px`;
      if (optionalDropdown) {
        optionalDropdown.style.left = `${initialDropdownX + tableDelta}px`;
      }
    };
    this._addEventListener("mousemove", window, resizeHeader);

    // Mouse or keyboard events : stop resize
    const stopResize = (ev) => {
      // Ignores the initial 'left mouse button down' event in order
      // to not instantly remove the listener
      if (ev.type === "mousedown" && ev.which === 1) {
        return;
      }
      ev.preventDefault();
      ev.stopPropagation();
      // We need a small timeout to not trigger a click on column header
      clearTimeout(this.resizeTimeout);
      this.resizeTimeout = setTimeout(() => {
        this.isResizing = false;
      }, 100);
      window.removeEventListener("mousemove", resizeHeader);
      table.classList.remove("o_resizing");
      resizingColumnElements.forEach((el) =>
        el.classList.remove("o_column_resizing")
      );
      resizeStoppingEvents.forEach((stoppingEvent) => {
        window.removeEventListener(stoppingEvent, stopResize);
      });

      const sizeColTable = JSON.parse(
        localStorage.getItem("sizeColTable") || "[]"
      );
      const inx = sizeColTable.findIndex(
        (i) =>
          i.model === this.state.model &&
          i.hasOwnProperty(th.getAttribute("data-name"))
      );
      const newSizeColTable = JSON.parse(JSON.stringify(sizeColTable));

      if (inx >= 0) {
        const d = {
          model: this.state.model,
          [th.getAttribute("data-name")]: th.offsetWidth,
        };
        newSizeColTable[inx] = d;
      } else {
        const d = {
          model: this.state.model,
          [th.getAttribute("data-name")]: th.offsetWidth,
        };
        newSizeColTable.push(d);
      }
      localStorage.setItem("sizeColTable", JSON.stringify(newSizeColTable));

      // we remove the focus to make sure that the there is no focus inside
      // the tr.  If that is the case, there is some css to darken the whole
      // thead, and it looks quite weird with the small css hover effect.
      document.activeElement.blur();
    };
    // We have to listen to several events to properly stop the resizing function. Those are:
    // - mousedown (e.g. pressing right click)
    // - mouseup : logical flow of the resizing feature (drag & drop)
    // - keydown : (e.g. pressing 'Alt' + 'Tab' or 'Windows' key)
    resizeStoppingEvents.forEach((stoppingEvent) => {
      this._addEventListener(stoppingEvent, window, stopResize);
    });
  },
});
