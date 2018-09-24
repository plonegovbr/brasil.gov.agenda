import DatePicker from './datepicker.js';


let zfill = (number, size=2) => (Array(size).fill('0').join('') + number).slice(-1 * size);


export default class AgendaTile {
  constructor(tile) {
    this.tile = tile;
    this.pageSize = 3;
    this.datepicker = new DatePicker(this.tile, this.onDateChange.bind(this));
    this.initSwiper();
    this.$('.is-now').append('<div class="now">Agora</div>')
    this.$('.daypicker').on('click', '.day', this.onDayClick.bind(this));
  }
  $(selector) {
    return $(selector, this.tile);
  }
  onDateChange(agendaDiaria) {
    this.swiper.removeAllSlides();
    let $slide = $('<div class="swiper-slide"></div>');
    if (agendaDiaria.hasAppointment === false) {
      $slide.addClass('no-events');
      $slide.html('Sem compromissos oficiais.');
      this.swiper.appendSlide($slide);
      return;
    }
    for (let compromisso of agendaDiaria.items) {
      if ($slide.children().length === this.pageSize) {
        this.swiper.appendSlide($slide);
        $slide = $('<div class="swiper-slide"></div>');
      }
      let $item = $(`
        <div class="collection-events-item">
          <a class="title-item" href="${compromisso.href}">${compromisso.title}</a>` +
          (compromisso.location == null? '' : `<div class="location-item">
            <span class="location">${compromisso.location}</span>
          </div>`) +
          `<div class="timestamp-cell">
            <span class="timestamp">
              ${compromisso.start}
            </span>
          </div>
        </div>
      `);
      if (compromisso.isNow) {
        $('.timestamp-cell', $item).addClass('is-now');
        $('.timestamp-cell', $item).append('<div class="now">Agora</div>')
      }
      $slide.append($item);
    }
    if ($slide.children().length > 0) {
      this.swiper.appendSlide($slide);
    }
  }
  initSwiper() {
    this.swiper = new Swiper(`#${this.tile.id} .collection-events`, {
      navigation: {
        nextEl: `#${this.tile.id} .collection-events .swiper-button-next`,
        prevEl: `#${this.tile.id} .collection-events .swiper-button-prev`,
      },
      pagination: {
        el: `#${this.tile.id} .collection-events .swiper-pagination`,
        clickable: true,
      },
    });
  }
  /**
   * Update day picker
   * Recreate list of days when ajax finish
   **/
  updateDayPicker(data) {
    this.datepicker.$day.html('');
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
      this.datepicker.$day.append($day);
    }
  }
  /**
   * Day Click Event
   * When click a day need to show the appointments of selected day, and upgate the list of days
   **/
  onDayClick(e) {
    e.preventDefault();
    let day = e.target;
    if (day.tagName !== 'LI') {
      day = day.parentElement;
    }
    let date = new Date(day.getAttribute('data-day'))
    this.datepicker.year = date.getFullYear();
    this.datepicker.month = date.getMonth();
    this.datepicker.day = date.getDate();
    this.datepicker.$currentPicker.datepicker('setDate', date);

    let agendaDiariaURL = `${this.datepicker.year}-${zfill(this.datepicker.month + 1)}-${zfill(this.datepicker.day)}`;
    $.ajax({
      url: `${this.datepicker.agendaURL}/json/${agendaDiariaURL}`,
      context: this,
      global: false,
    }).always(function(data) {
      this.updateDayPicker(data);
      this.onDateChange(data[3]);
      this.datepicker.daysWithAppointments = data[3].daysWithAppointments;
      this.datepicker.updateMonthPicker();
    });
  }
}
