let range = (start, stop, step=1) => Array(stop - start).fill(start).map((x, y) => x + y * step);
let zfill = (number, size=2) => (Array(size).fill('0').join('') + number).slice(-1 * size);


export default class DatePicker {
  constructor(container, callback) {
    this.container = container;
    this.callback = callback;
    this.agendaURL = container.getAttribute('data-url');
    this.$month = this.$('.monthpicker .month');
    this.$year = this.$('.monthpicker .year');
    this.$day = this.$('.daypicker')
    this.$datePicker = this.$('.monthpicker input');
    this.$datePicker3 = this.$('.calendar');
    this.isMobile = false;
    this.is3calendar = false;
    if (this.$datePicker[0] == null) {
      this.is3calendar = true;
    }
    this.$currentPicker = this.is3calendar ? this.$datePicker3 : this.$datePicker;
    this.daysWithAppointments = []
    this.initMonthPicker();
    let today = new Date();
    this.year = today.getFullYear();
    this.month = today.getMonth();
    this.day = today.getDate();
    $(window).resize(this.resize.bind(this));
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
    $.ajax({
      url: `${this.agendaURL}/json/${agendaDiariaURL}`,
      context: this,
      global: false,
    }).always(function(data) {
      if (typeof this.callback === 'function') {
        this.callback(data);
      }
      this.daysWithAppointments = [];
      if (data[3].daysWithAppointments != null) {
        this.daysWithAppointments = data[3].daysWithAppointments;
      }
      this.updateMonthPicker();
    });
  }
  updateMonthPicker() {
    this.$currentPicker.datepicker('setDate', new Date(this.year, this.month, this.day));
    if (this.is3calendar === false) {
      let monthNamesShort = this.$currentPicker.datepicker('option', 'monthNamesShort');
      this.$month.html(monthNamesShort[this.month].toUpperCase());
      this.$year.html(this.year);
      $('.monthpicker').attr('data-month', this.month);
      $('.monthpicker').attr('data-year', this.year);
      this.fixCalendarTitle();
    }
    if (this.is3calendar === true) {
      this.resize();
    }
  }
  resize(e) {
    let isMobile = ($(window).width() <= 767);
    // if it is called by resize event and responsive don't change
    if (e != null && this.isMobile === isMobile) {
      return;
    }
    this.isMobile = isMobile;
    let showCurrentAtPos = 1;
    let numberOfMonths = 3;
    if (isMobile) {
      showCurrentAtPos = 0;
      numberOfMonths = 1;
    }
    this.$currentPicker.datepicker('option', 'numberOfMonths', numberOfMonths);
    this.$currentPicker.datepicker('option', 'showCurrentAtPos', showCurrentAtPos);
    setTimeout(function() {
      this.$currentPicker.datepicker('option', 'showCurrentAtPos', showCurrentAtPos);
    }.bind(this), 1);
    this.fixCalendarTitle();
  }
  fixCalendarTitle() {
    $('.ui-datepicker-title').removeClass('loaded');
    setTimeout(function() {
      for (let month of $('.ui-datepicker-month')) {
        month.textContent = month.textContent.slice(0, 3);
      }
      $('.ui-datepicker-title').addClass('loaded');
    }, 1);
  }
  initMonthPicker() {
    // this event is needed to get right translation
    $(window).on('load', function() {
      let onSelect = function(dateText, inst) {
        this.year = inst.selectedYear;
        this.month = inst.selectedMonth;
        this.day = parseInt(inst.selectedDay);
        if (this.is3calendar === true) {
          // Faz com que o datepicker não seja recarregado antes do
          // redirecionamento, evitando que o mês atual seja deslocado para o
          // terceiro calendário. Ver:
          // https://github.com/jquery/jquery-ui/blob/1.10.2/ui/jquery.ui.datepicker.js#L1014-L1015
          inst.inline = false;
          // https://stackoverflow.com/a/19374679
          window.location = `${this.agendaURL}/${this.year}-${zfill(this.month + 1)}-${zfill(this.day)}`;
        } else {
          this.update();
        }
      };
      let beforeShowDay = function(date) {
        let day = date.toISOString().slice(0, 10);
        if (this.daysWithAppointments.indexOf(day) >= 0) {
          return [true, 'ui-has-appointments', ''];
        }
        return [false, '', ''];
      };
      let onChangeMonthYear = function(year, month, inst) {
        this.year = inst.selectedYear;
        this.month = inst.selectedMonth;
        this.day = parseInt(inst.selectedDay);
        this.update();
      };
      let options = {
        onSelect: onSelect.bind(this),
        beforeShowDay: beforeShowDay.bind(this),
        onChangeMonthYear: onChangeMonthYear.bind(this),
      };
      if (this.is3calendar) {
        options.numberOfMonths = 3;
      } else {
        options.beforeShow = this.fixCalendarTitle.bind(this);
      }
      this.$currentPicker.datepicker(options);
      this.update();
    }.bind(this));
  }
}
