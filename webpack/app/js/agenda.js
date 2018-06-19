import DatePicker from './datepicker.js';


let zfill = (number, size=2) => (Array(size).fill('0').join('') + number).slice(-1 * size);


export default class AgendaView {
  constructor(container) {
    this.container = container;
    this.datepicker = new DatePicker(container, this.onDateChange.bind(this), true);
    this.$appointments = this.$('.list-compromissos');
  }
  $(selector) {
    return $(selector, this.container.parentElement);
  }
  extractTime(dateTime) {
    let [, time] = dateTime.split('T');
    let [hours, minutes, ] = time.split(':');
    return `${zfill(hours)}h${zfill(minutes)}`;
  }
  onDateChange(agendaDiaria) {
    this.$appointments.html('');
    if (agendaDiaria.hasAppointment === false) {
      this.$appointments.append(`
        <li class="sem-compromisso item-compromisso">
          <span>Atualmente não existem compromissos agendados.</span>
        </li>
      `);
      return;
    }
    for (let compromisso of agendaDiaria.items) {
      let $item = $(`
        <li class="item-compromisso-wrapper">
          <div class="item-compromisso">
            <div class="compromisso-horarios">
              <time class="horario compromisso-inicio"
                    datetime="${compromisso.datetime}">
                ${compromisso.start}
              </time>
            </div>
            <div class="compromisso-dados">
              <h4 class="compromisso-titulo">${compromisso.title}</h4>` +
              (compromisso.location == null? '': `<p class="compromisso-local">${compromisso.location}</p>`) +
              `<span class="download-compromisso">
                <a class="add-agenda vcal" href="${compromisso.vcal}">VCAL</a>
                <span>Adicionar ao meu calendário</span>
              </span>
            </div>
          </div>
        </li>
      `);
      if (compromisso.isNow) {
        $('.compromisso-horarios', $item).append('<div class="now">Agora</div>');
      }
      this.$appointments.append($item);
    }
  }
}
