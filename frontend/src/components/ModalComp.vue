

<script>
/* eslint-disable */
export default {
  name: "ModalComp",
  props: {
    form: {
      type: Object,
      default: () => {
        return {};
      }
    },
    show: {
      type: Boolean,
      default: false,
    }
  },
  emits: ['onHide', 'onSave', 'onDelete'],
  computed: {
    onShow() {
      return {'fade show': this.show};
    },
  },
  methods: {
    onHideClick() {
      this.$emit('onHide');
    },
    onDeleteClick() {
      this.$emit('onDelete');
    },
    onSaveClick() {
      this.$emit('onSave');
    }
  }
}
</script>
<template>
  <div
      v-if="show"
      class="modal fade show"
      tabindex="-1"
      role="dialog"
      aria-labelledby="exampleModalLiveLabel"
      style="display: block; padding-right: 17px;"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ form.name }} {{ form.last_name }}</h5>
          <button
              @click.prevent="onHideClick"
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
          >
            <span aria-hidden="true">×</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row mt-2">
            <div class="col-12">
              <label for="date" class="form-label">Fecha</label>
              <input id="date" type="date" class="form-control" v-model="form.schedule_date" />
            </div>
          </div>
          <div class="row mt-2">
            <div class="col-12">
              <label for="time" class="form-label">Hora</label>
              <input id="time" type="time" class="form-control" v-model="form.schedule_time" />
            </div>
          </div>
          <div class="row mt-2">
            <div class="col-12">
              <label class="form-label">Motivo</label>
              <textarea v-model="form.reason" class="form-control" disabled></textarea>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
              @click="onDeleteClick"
              type="button"
              class="btn btn-danger"
              data-dismiss="modal"
          >
            Eliminar
          </button>
          <button
              @click="onHideClick"
              type="button"
              class="btn btn-secondary"
              data-dismiss="modal"
          >
            Cancelar
          </button>
          <button
              @click="onSaveClick"
              type="button"
              class="btn btn-primary"
          >
            Guardar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
