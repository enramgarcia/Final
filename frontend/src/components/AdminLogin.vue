<template>
  <div class="mx-auto">
    <div class="row mt-2">
      <div class="col-md-4 mx-auto alert alert-warning">
        Este es un ambiente de prueba<br>
        <b>user</b>: admin<br>
        <b>password</b>: 123456
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-md-4 mx-auto">
        <label for="username" >Usuario</label>
        <input id="username" v-model="form.username" type="text" class="form-control" />
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-md-4 mx-auto">
        <label for="password" >Password</label>
        <input id="password" v-model="form.password" type="password" class="form-control" />
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-md-4 mx-auto">
        <button @click.prevent="onLogin" class="btn btn-primary d-block">Iniciar Sesion</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdminLogin",
  data() {
    return {
      form: {
        username: null,
        password: null,
      }
    };
  },
  created() {

  },
  methods: {
    onLogin() {
      axios.post('http://localhost:5000/admin/login', this.form)
          .then((response) => {
            localStorage.setItem('_token', response.data.token);
            this.$router.push('/');
          })
          .catch((err) => {
            alert(err.response.error.data);
          })
    }
  }
}
</script>
