let range = (start, stop, step=1) => Array(stop - start).fill(start).map((x, y) => x + y * step);


export default class DatePicker {
  constructor(container, callback) {
    this.container = container;
    this.callback = callback;
    this.$month = this.$('.monthpicker .month');
    this.$year = this.$('.monthpicker .year');
    this.$day = this.$('.daypicker')
    this.$monthInput = this.$('.monthpicker input');
    this.initMonthPicker();
    let today = new Date();
    this.year = today.getFullYear();
    this.month = today.getMonth();
    this.day = today.getDate();
    this.$('.daypicker').on('click', '.day', this.onDayClick.bind(this));
  }
  $(selector) {
    return $(selector, this.container);
  }
  update() {
    this.updateMonthPicker();
    this.updateDayPicker();
    if (typeof this.callback === 'function') {
      // ajax
      this.callback();
    }
  }
  updateMonthPicker() {
    let monthNamesShort = this.$monthInput.datepicker('option', 'monthNamesShort');
    this.$month.html(monthNamesShort[this.month].toUpperCase());
    this.$year.html(this.year);
    $('.monthpicker').attr('data-month', this.month);
    $('.monthpicker').attr('data-year', this.year);
  }
  updateDayPicker() {
    let dayNamesShort = this.$monthInput.datepicker('option', 'dayNamesShort');
    let days = range(-3, 4).map(i => new Date(this.year, this.month, this.day + i))
    this.$day.html('');
    for (let day of days) {
      let cssclass = ['day'];
      if (day.getFullYear() === this.year  &&
          day.getMonth()    === this.month &&
          day.getDate()     === this.day)  {
        cssclass.push('is-selected');
      }
      this.$day.append(`
        <li data-day="${day.toISOString()}" class="${cssclass.join(' ')}">
          <div class="daypicker-day">${day.getDate()}</div>
          <div class="daypicker-weekday">${dayNamesShort[day.getDay()]}</div>
        </li>
      `);
    }
  }
  initMonthPicker() {
    this.$monthInput.datepicker( {
      changeMonth: true,
      changeYear: true,
      showButtonPanel: true,
      onChangeMonthYear: (month, year, inst) => {
        $('#ui-datepicker-div').addClass('ui-selected');
      },
      onClose: function(dateText, inst) { 
        if (!$('#ui-datepicker-div').hasClass('ui-selected')) {
          return;
        }
        $('#ui-datepicker-div').removeClass('ui-selected');
        this.year = inst.selectedYear;
        this.month = inst.selectedMonth;
        this.$monthInput.datepicker('setDate', new Date(this.year, this.month, this.day));
        this.update();
      }.bind(this),
      beforeShow: (input, inst) => {
        $('#ui-datepicker-div').addClass('ui-monthpicker');
      }
    });
  }
  onDayClick(e) {
    e.preventDefault();
    let day = e.target;
    if (day.tagName !== 'LI') {
      day = day.parentElement;
    }
    let date = new Date(day.getAttribute('data-day'))
    this.year = date.getFullYear();
    this.month = date.getMonth();
    this.day = date.getDate();
    this.$monthInput.datepicker('setDate', date);
    this.update();
  }
}
