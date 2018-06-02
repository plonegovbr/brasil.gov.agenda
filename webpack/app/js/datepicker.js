let range = (start, stop, step=1) => Array(stop - start).fill(start).map((x, y) => x + y * step);
let zfill = (number, size=2) => (Array(size).fill('0').join('') + number).slice(-1 * size);


export default class DatePicker {
  constructor(container, callback, updateTitle=false) {
    this.container = container;
    this.agendaURL = container.getAttribute('data-url');
    this.callback = callback;
    this.updateTitle = updateTitle;
    this.$month = this.$('.monthpicker .month, .calendar-title .strmonth');
    this.$year = this.$('.monthpicker .year, .calendar-title .year');
    this.$day = this.$('.daypicker')
    this.$datePicker = this.$('.monthpicker input');
    this.$datePicker3 = this.$('.calendar');
    this.$currentPicker = this.$datePicker.length > 0 ? this.$datePicker : this.$datePicker3;
    this.initMonthPicker();
    let today = new Date();
    this.year = today.getFullYear();
    this.month = today.getMonth();
    this.day = today.getDate();
    this.$('.daypicker').on('click', '.day', this.onDayClick.bind(this));
    if ($('.portaltype-agendadiaria').length > 0) {
      let pathDate = location.pathname.split('/').pop();
      let [year, month, day] = pathDate.split('-').map(x => parseInt(x));
      let date = new Date(year, month - 1, day);
      this.year = date.getFullYear();
      this.month = date.getMonth();
      this.day = date.getDate();
    }
  }
  $(selector) {
    return $(selector, this.container);
  }
  update() {
    this.updateMonthPicker();
    this.updateDayPicker();
    let agendaDiariaURL = `${this.year}-${zfill(this.month + 1)}-${zfill(this.day)}`;
    if (typeof this.callback === 'function') {
      $.ajax({
        headers: {
          Accept: 'application/json'
        },
        global: false,
        url: `${this.agendaURL}/${agendaDiariaURL}`,
      }).always(this.callback);
    }
    if (this.updateTitle) {
      let agendaDiaria = `${zfill(this.day)}/${zfill(this.month + 1)}/${this.year}`;
      let title = `Agenda de ${$('.documentFirstHeading').text().trim()} para ${agendaDiaria}`;
      window.history.pushState(
        {day: this.day, month: this.month, year: this.year},
        title,
        `${this.agendaURL}/${agendaDiariaURL}?month:int=${this.month + 1}&year:int=${this.year}`
      );
      document.title = title;
    }
  }
  updateMonthPicker() {
    this.$currentPicker.datepicker('setDate', new Date(this.year, this.month, this.day));
    if (this.$datePicker.length > 0) {
      let monthNamesShort = this.$currentPicker.datepicker('option', 'monthNamesShort');
      this.$month.html(monthNamesShort[this.month].toUpperCase());
      this.$year.html(this.year);
      $('.monthpicker').attr('data-month', this.month);
      $('.monthpicker').attr('data-year', this.year);
    }
    if (this.$datePicker3.length > 0) {
      let monthNames = this.$currentPicker.datepicker('option', 'monthNames');
      this.$currentPicker.datepicker('option', 'showCurrentAtPos', 1);
      setTimeout(function() {
        this.$currentPicker.datepicker('option', 'showCurrentAtPos', 1);
      }.bind(this), 1);
      this.$month.html(monthNames[this.month].toUpperCase());
      this.$year.html(this.year);
    }
  }
  updateDayPicker() {
    let dayNamesShort = this.$currentPicker.datepicker('option', 'dayNamesShort');
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
        global: false,
        context: $day,
      }).done(function(result) {
        this.addClass('has-appointment');
      });

      this.$day.append($day);
    }
    // rfs
  }
  initMonthPicker() {
    // this event is needed to get right translation
    $(window).on('load', function() {
      let onSelect = function(dateText, inst) { 
        this.year = inst.selectedYear;
        this.month = inst.selectedMonth;
        this.day = parseInt(inst.selectedDay);
        this.update();
      }.bind(this);
      this.$datePicker.datepicker( {
        onSelect: onSelect,
      });
      this.$datePicker3.datepicker( {
        numberOfMonths: 3,
        onSelect: onSelect,
      });
      this.update();
    }.bind(this));
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
    this.$currentPicker.datepicker('setDate', date);
    this.update();
  }
}