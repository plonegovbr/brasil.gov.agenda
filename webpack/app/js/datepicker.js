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
    this.daysWithAppointments = []
    this.initMonthPicker();
    let today = new Date();
    this.pageLoad = true;
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
    let agendaDiariaURL = `${this.year}-${zfill(this.month + 1)}-${zfill(this.day)}`;
    if (typeof this.callback === 'function') {
      $.ajax({
        url: `${this.agendaURL}/json/${agendaDiariaURL}`,
        context: this,
        global: false,
      }).always(function(data) {
        this.callback(data[3]);
        this.updateDayPicker(data);
        this.daysWithAppointments = data[3].daysWithAppointments;
        this.updateMonthPicker();
      });
    }
    // we don't want to change URL when page load
    if (this.updateTitle && ! this.pageLoad) {
      let agendaDiaria = `${zfill(this.day)}/${zfill(this.month + 1)}/${this.year}`;
      let title = `Agenda de ${$('.documentFirstHeading').text().trim()} para ${agendaDiaria}`;
      window.history.pushState(
        {day: this.day, month: this.month, year: this.year},
        title,
        `${this.agendaURL}/${agendaDiariaURL}`
      );
      document.title = title;
    }
    this.pageLoad = false;
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
  updateDayPicker(data) {
    this.$day.html('');
    for (let day of data) {
      let cssclass = ['day'];
      if (day.isSelected) {
        cssclass.push('is-selected');
      }
      let $day = $(`
        <li data-day="${day.datetime}" class="${cssclass.join(' ')}">
          <div class="daypicker-day">${day.day}</div>
          <div class="daypicker-weekday">${day.weekday}</div>
        </li>
      `);
      if (day.hasAppointment) {
        $day.addClass('has-appointment');
      }
      this.$day.append($day);
    }
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
      let beforeShowDay = function(date) { 
        let day = date.toISOString().slice(0, 10);
        if (this.daysWithAppointments.indexOf(day) >= 0) {
          return [true, 'ui-has-appointments', ''];
        }
        return [true, '', ''];
      }.bind(this);
      this.$datePicker.datepicker( {
        onSelect: onSelect,
        beforeShowDay: beforeShowDay,
      });
      this.$datePicker3.datepicker( {
        numberOfMonths: 3,
        onSelect: onSelect,
        beforeShowDay: beforeShowDay,
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
