<template>
  <modal-comp
      :form="currentEvent"
      :show="showModal"
      @onHide="showModal = false"
      @onSave="onSave"
      @onDelete="onDelete"
  />
  <template v-if="showCalendar">
    <div v-if="loggedIn" class="row mb-2">
      <div class="col-12">
        <div class="float-end">
          <router-link to="/settings">Config.</router-link>
        </div>
      </div>
    </div>
    <FullCalendar :options="calendarOptions" />
  </template>
  <template v-else>
    <div v-if="loggedIn" class="row mb-2">
      <div class="col-12">
        <div class="float-end">
          <button @click.prevent="showCalendar = true" class="btn btn-link">Calendario</button>
        </div>
      </div>
    </div>
    <h1>{{ form.selectedDate }}</h1>
    <form @submit.prevent="onSend">

      <div class="row mt-3">
        <div class="col-12 col-md-6">
          <div class="row mt-2">
            <div class="col-12 col-md-6">
              <label for="name" class="form-label">Nombre</label>
              <input id="name" class="form-control" v-model="form.name "/>
            </div>
            <div class="col-12 col-md-6">
              <label for="last_name" class="form-label">Apellido</label>
              <input id="last_name" class="form-control" v-model="form.lastName" />
            </div>
          </div>
          <div class="row mt-2">
            <div class="col-12">
              <label for="email" class="form-label">E-mail</label>
              <input id="email" class="form-control" v-model="form.email" />
            </div>
          </div>
          <div class="row mt-2">
            <div class="col-12 col-md-6">
              <label for="phone" class="form-label">Teléfono</label>
              <input id="phone" class="form-control" v-model="form.phone" />
            </div>
          </div>
          <div class="row mt-2">
            <div class="col-12">
              <label class="form-label">Razón</label>
              <textarea class="form-control" rows="5" v-model="form.reason" />
            </div>
          </div>
        </div>
        <div class="col-12 col-md-4">
          <div
              v-for="(availableTime, index) in availableTimes"
              :key="index"
              class="row mt-2"
          >
            <input
                type="radio"
                class="btn-check"
                :id="'time' + index"
                name="times"
                v-model="form.selectedTime"
                :value="availableTime"
                autocomplete="off">
            <label class="btn btn-outline-primary" :for="'time' + index">
              {{ availableTime }}
            </label>
          </div>

        </div>
      </div>
      <div class="row mt-3">
        <div class="col-12">
          <div class="float-end">
            <button class="btn btn-primary">Agendar</button>
          </div>
        </div>
      </div>
    </form>
  </template>
</template>

<script>

import axios from 'axios';
import '@fullcalendar/core/vdom'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import ModalComp from "@/components/ModalComp";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "CalendarComp",
  components: {
    ModalComp,
    FullCalendar
  },
  data() {
    return {
      loggedIn: false,
      showModal: false,
      events: [],
      currentEvent: {},
      showCalendar: true,
      availableTimes: [],
      calendarOptions: {
        plugins: [ dayGridPlugin, interactionPlugin ],
        initialView: 'dayGridMonth',
        dateClick: this.handleDateClick,
        eventClick: this.handleEventClick,
        events: [],
      },
      form: {
        selectedDate: null,
        selectedTime: null,
        name: null,
        lastName: null,
        email: null,
        phone: null,
        reason: null,
      }
    }
  },
  created() {

    if (localStorage.getItem('_token') === null) {
      return;
    }

    this.loggedIn = true;
    this.fetchSchedules();
  },
  methods: {
    handleDateClick(ev) {
      this.form.selectedDate = ev.dateStr;
      this.fetchTimes();
    },
    handleEventClick(ev) {
      axios.get('http://localhost:5000/admin/schedules/' + ev.event.id, this.getToken())
          .then(response => {
            this.currentEvent = response.data.schedule;
            this.showModal = true;
          })
          .catch(err => {
            alert(err.response.data.error);
            this.deleteToken(err.response);
          });
    },
    getToken() {
      return {
        headers: {
          'Authorization': 'JWT ' + localStorage.getItem('_token')
        }
      };
    },
    deleteToken(response) {
      if (response.status !== 401) {
        return;
      }

      localStorage.removeItem('_token');
      this.loggedIn = false;
    },
    fetchSchedules() {
      axios.get('http://localhost:5000/admin/schedules', this.getToken())
          .then(response => {
            this.calendarOptions.events = response.data;
          })
          .catch(err => {
            alert(err.response.data.error);
            this.deleteToken(err.response);
          });
    },
    fetchData() {
      axios.get('http://localhost:5000/schedules')
          .then(response => {
            this.events = response.data;
          })
          .catch(err => {
            alert(err.response.data.error);
          });
    },
    fetchTimes() {
      axios.get('http://localhost:5000/schedules/create?date=' + this.form.selectedDate)
          .then(response => {
            this.showCalendar = false;
            this.availableTimes = response.data.times;
          })
          .catch(err => {
            alert(err.response.data.error);
          });
    },
    onSend() {
      axios.post('http://localhost:5000/schedules/create', this.form)
          .then(() => {
            alert('Se ha creado la cita exitosamente.')

            if (this.loggedIn) {
              this.fetchSchedules();
            }

            this.showCalendar = true;
          })
          .catch(err => {
            alert(err.response.data.error);
          });
    },
    onSave() {
      axios.post('http://localhost:5000/admin/schedules/' + this.currentEvent.id + '/edit', this.currentEvent, this.getToken())
          .then(() => {
            this.fetchSchedules();
            this.showModal = false;
            this.currentEvent = {};
          })
          .catch(err => {
            alert(err.response.data.error);
            this.deleteToken(err.response);
          });
    },
    onDelete() {
      axios.delete('http://localhost:5000/admin/schedules/' + this.currentEvent.id, this.getToken())
          .then(() => {
            this.fetchSchedules();
            this.showModal = false;
            this.currentEvent = {};
          })
          .catch(err => {
            alert(err.response.data.error);
            this.deleteToken(err.response);
          });
    },
  }
}
</script>
