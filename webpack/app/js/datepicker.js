let range = (start, stop, step=1) => Array(stop - start).fill(start).map((x, y) => x + y * step);
let zfill = (number, size=2) => (Array(size).fill('0').join('') + number).slice(-1 * size);


export default class DatePicker {
  constructor(container, callback) {
    this.container = container;
    this.agendaURL = container.getAttribute('data-url');
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
      let agendaDiaria = `${this.year}-${zfill(this.month + 1)}-${zfill(this.day)}`;
      $.ajax({
        headers: {
          Accept: 'application/json'
        },
        url: `${this.agendaURL}/${agendaDiaria}`,
      }).always(this.callback);
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
    // get a list with 3 days before and 3 days after current day
    let days = range(-3, 4).map(i => new Date(this.year, this.month, this.day + i))
    this.$day.html('');
    for (let day of days) {
      let cssclass = ['day'];
      if (day.getFullYear() === this.year  &&
          day.getMonth()    === this.month &&
          day.getDate()     === this.day)  {
        cssclass.push('is-selected');
      }

      let $day = $(`
        <li data-day="${day.toISOString()}" class="${cssclass.join(' ')}">
          <div class="daypicker-day">${day.getDate()}</div>
          <div class="daypicker-weekday">${dayNamesShort[day.getDay()]}</div>
        </li>
      `);

      let agendaDiaria = `${day.getFullYear()}-${zfill(day.getMonth() + 1)}-${zfill(day.getDate())}`;
      $.ajax({
        headers: {
          Accept: 'application/json'
        },
        url: `${this.agendaURL}/${agendaDiaria}`,
        context: $day,
      }).done(function(result) {
        this.addClass('has-appointment');
      });

      this.$day.append($day);
    }
  }
  initMonthPicker() {
    this.$monthInput.datepicker( {
      changeMonth: true,
      changeYear: true,
      showButtonPanel: true,
      onSelect: function(dateText, inst) { 
        this.year = inst.selectedYear;
        this.month = inst.selectedMonth;
        this.day = parseInt(inst.selectedDay);
        this.$monthInput.datepicker('setDate', new Date(this.year, this.month, this.day));
        this.update();
      }.bind(this),
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
