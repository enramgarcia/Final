<template>
  <div class="float-end">
    <router-link to="/">Calendario</router-link>
  </div>
  <h1>Configuración</h1>
  <form @submit.prevent="onSubmitSettings">
    <div class="row mt-2">
      <div class="col-md-6">
        <label for="systemEmail" class="form-label">E-mail Sistema</label>
        <input id="systemEmail" type="text" class="form-control" v-model="form.systemEmail" />
      </div>
      <div class="col-md-6">
        <label for="businessName" class="form-label">Nombre Negocio</label>
        <input id="businessName" type="text" class="form-control" v-model="form.businessName" />
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-md-6">
        <label for="sundayStart" class="form-label">Inicio Domingo</label>
        <input id="sundayStart" type="time" class="form-control" v-model="form.sundayStart" />
      </div>
      <div class="col-md-6">
        <label for="sundayStart" class="form-label">Fin Domingo</label>
        <input id="sundayStart" type="time" class="form-control" v-model="form.sundayEnd" />
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-md-6">
        <label for="mondayStart" class="form-label">Inicio Lunes</label>
        <input id="mondayStart" type="time" class="form-control" v-model="form.mondayStart" />
      </div>
      <div class="col-md-6">
        <label for="mondayStart" class="form-label">Fin Lunes</label>
        <input id="mondayStart" type="time" class="form-control" v-model="form.mondayEnd" />
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-md-6">
        <label for="tuesdayStart" class="form-label">Inicio Martes</label>
        <input id="tuesdayStart" type="time" class="form-control" v-model="form.tuesdayStart" />
      </div>
      <div class="col-md-6">
        <label for="tuesdayStart" class="form-label">Fin Martes</label>
        <input id="tuesdayStart" type="time" class="form-control" v-model="form.tuesdayEnd" />
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-md-6">
        <label for="wednesdayStart" class="form-label">Inicio Miercoles</label>
        <input id="wednesdayStart" type="time" class="form-control" v-model="form.wednesdayStart" />
      </div>
      <div class="col-md-6">
        <label for="wednesdayStart" class="form-label">Fin Miercoles</label>
        <input id="wednesdayStart" type="time" class="form-control" v-model="form.wednesdayEnd" />
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-md-6">
        <label for="thursdayStart" class="form-label">Inicio Jueves</label>
        <input id="thursdayStart" type="time" class="form-control" v-model="form.thursdayStart" />
      </div>
      <div class="col-md-6">
        <label for="thursdayStart" class="form-label">Fin Jueves</label>
        <input id="thursdayStart" type="time" class="form-control" v-model="form.thursdayEnd" />
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-md-6">
        <label for="fridayStart" class="form-label">Inicio Viernes</label>
        <input id="fridayStart" type="time" class="form-control" v-model="form.fridayStart" />
      </div>
      <div class="col-md-6">
        <label for="fridayStart" class="form-label">Fin Viernes</label>
        <input id="fridayStart" type="time" class="form-control" v-model="form.fridayEnd" />
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-md-6">
        <label for="saturdayStart" class="form-label">Inicio Sabado</label>
        <input id="saturdayStart" type="time" class="form-control" v-model="form.saturdayStart" />
      </div>
      <div class="col-md-6">
        <label for="saturdayStart" class="form-label">Fin Sabado</label>
        <input id="saturdayStart" type="time" class="form-control" v-model="form.saturdayEnd" />
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-12">
        <div class=" float-lg-end">
          <button class="btn btn-primary">Guardar</button>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
import axios from "axios";

export default {
  name: 'SettingsComp',
  data() {
    return {
      form: {
        sundayStart: null,
        sundayEnd: null,
        mondayStart: null,
        mondayEnd: null,
        tuesdayStart: null,
        tuesdayEnd: null,
        wednesdayStart: null,
        wednesdayEnd: null,
        thursdayStart: null,
        thursdayEnd: null,
        fridayStart: null,
        fridayEnd: null,
        saturdayStart: null,
        saturdayEnd: null,
        businessName: null,
        systemEmail: null,
      }
    }
  },
  created() {
    this.fetchSettings()
  },
  methods: {
    fetchSettings() {

      axios.get('http://localhost:5000/settings')
          .then(res => {
            const resData = res.data;
            this.form.sundayStart = resData.sunday_start;
            this.form.sundayEnd = resData.sunday_end;
            this.form.mondayStart = resData.monday_start;
            this.form.mondayEnd = resData.monday_end;
            this.form.tuesdayStart = resData.tuesday_start;
            this.form.tuesdayEnd = resData.tuesday_end;
            this.form.wednesdayStart = resData.wednesday_start;
            this.form.wednesdayEnd = resData.wednesday_end;
            this.form.thursdayStart = resData.thursday_start;
            this.form.thursdayEnd = resData.thursday_end;
            this.form.fridayStart = resData.friday_start;
            this.form.fridayEnd = resData.friday_end;
            this.form.staurdayStart = resData.saturday_start;
            this.form.staurdayEnd = resData.staurday_end;
            this.form.businessName = resData.business_name;
            this.form.systemEmail = resData.system_email;
          })
          .catch(err => {
            console.error(err)
          })
    },
    onSubmitSettings() {
      axios.post('http://localhost:5000/settings/create', this.form)
          .then(() => {
            alert('Se ha guardado exitosamente.')
          })
          .catch(err => {
            console.error(err);
          })
    }
  }
}
</script>
