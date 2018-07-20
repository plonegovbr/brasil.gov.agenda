import DatePicker from './datepicker.js';


let zfill = (number, size=2) => (Array(size).fill('0').join('') + number).slice(-1 * size);


export default class AgendaView {
  constructor(container) {
    this.container = container;
    this.datepicker = new DatePicker(container, this.onDateChange.bind(this), true);
    this.$appointments = this.$('.list-compromissos');
    this.editable = container.dataset.editable === 'True';
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
    let $item, $edit;
    this.$appointments.html('');
    this.$('.portalMessage.info').html(agendaDiaria.update);
    if (agendaDiaria.hasAppointment === false) {
      this.$appointments.append(`
        <li class="sem-compromisso item-compromisso">
          <span>Atualmente não existem compromissos agendados.</span>
        </li>
      `);
      return;
    }
    for (let compromisso of agendaDiaria.items) {
      $item = $(`
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
                <a class="add-agenda vcal" href="${compromisso.href}/vcal_view">VCAL</a>
                <span>Adicionar ao meu calendário</span>
              </span>
            </div>
          </div>
        </li>
      `);
      if (this.editable) {
        $edit = $(`
          <ul class="compromisso-acoes">
            <li class="compromisso-acao">
              <a class="compromisso editar_compromisso acao" href="${compromisso.href}/edit">Editar</a>
            </li>
            <li class="compromisso-acao">
              <a class="compromisso remover_compromisso acao" href="${compromisso.href}/delete_confirmation">Remover</a>
            </li>
          </ul>
        `);
        $('.editar_compromisso', $edit).prepOverlay({
          subtype: 'ajax',
          filter: common_content_filter,
          formselector: '#form',
          cssclass: 'overlay-compromisso',
          noform: function(el) {return $.plonepopups.noformerrorshow(el, 'redirect');},
          redirect: location.href,
          closeselector: '[name="form.buttons.cancel"]',
          width:'50%'
        });
        $('.remover_compromisso', $edit).prepOverlay({
          subtype: 'ajax',
          filter: common_content_filter,
          formselector: '#delete_confirmation',
          cssclass: 'overlay-compromisso',
          noform: function(el) {return $.plonepopups.noformerrorshow(el, 'redirect');},
          redirect: location.href,
          closeselector: '[name="form.button.Cancel"]',
          width:'50%'
        });
        $('.item-compromisso', $item).append($edit);
      }
      if (compromisso.isNow) {
        $('.compromisso-horarios', $item).append('<div class="now">Agora</div>');
      }
      this.$appointments.append($item);
    }
  }
}
