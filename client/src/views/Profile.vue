<template>
<div>
<b-navbar toggleable="lg" type="dark" variant="dark">
<b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
<b-collapse id="nav-collapse" is-nav>
  <b-navbar-nav>
  <b-nav-item href="/"><button type="button" class="btn btn-primary">
    Home</button></b-nav-item>
  <b-nav-item><button type="button" class="btn btn-primary"
    v-b-modal.addtemp-modal>
      Add Temperature
      </button></b-nav-item>
  <b-nav-item><button
    type="button"
    class="btn btn-primary"
    v-b-modal.edit-user-modal
    @click="editUser(user)">
    Edit User
    </button></b-nav-item>
  </b-navbar-nav>

  <!-- Right aligned nav items -->
  <b-navbar-nav class="ml-auto">
  </b-navbar-nav>
  </b-collapse>
  </b-navbar>
<div v-if="user.Success">
  <v-snackbar
      v-model="showDismissibleAlert"
      :timeout="timeout"
    >
      {{ message }}

      <template v-slot:action="{ attrs }">
        <v-btn
          color="blue"
          text
          v-bind="attrs"
          @click="showDismissibleAlert = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    <div class="alert alert-primary" role="alert">
      <strong>Name:</strong> {{ user.Name }}<br>
      <strong>RFID:</strong> {{ user.RFID }}<br>
      <strong>Barcode:</strong> {{ user.Barcode }}<br>
    </div>
    <div class="alert alert-warning" role="alert">
      <div style="text-align:center">
        <h3>Quick Information</h3>
      </div>
        <strong>Highest Temperature:</strong> {{ user.Highest_Temp.Temperature }}<br>
        <strong>Date:</strong> {{ user.Highest_Temp.Date }}<br><br>
        <strong>Average Temperature:</strong> {{ user.Average_Temp.Average }}<br><br>
        <strong>Lowest Temperature:</strong> {{ user.Lowest_Temp.Temperature }}<br>
        <strong>Date:</strong> {{ user.Lowest_Temp.Date }}
    </div>
    <div align="center">
    <h3>Temperature Graph - Most recent 14 entries (Ascending)</h3>
    </div>
    <BarGraph :bargraphseries="bargraphseries"/>
    <div class="alert alert-secondary" role="alert">
      <div style="text-align:center">
        <h3>Temperature Log</h3>
      </div>
      <input type="text"
         placeholder="Search temperatures"
         v-model="filter" />
      <v-data-table
        :headers="fields"
        :items="filteredRows"
        :items-per-page="10"
        class="elevation-1">
        <template v-slot:item="row">
          <tr>
            <td>
            <span v-if="row.item.HighTemp">
              <img src="../assets/hightemp.png"/>
            </span>
            <span v-else>
              <img src="../assets/lowtemp.png"/>
            </span>
            </td>
            <td>{{row.item.DateTime}}</td>
            <td>{{row.item.Temperature}}</td>
            <td>
            <div class="btn-group" role="group" aria-label="First group">
            <button
              type="button"
              class="btn btn-outline-primary btn-sm"
              v-b-modal.edit-temp-modal
              @click="editTemp(row.item)">
              Edit
            </button>
            <button
              type="button"
              class="btn btn-outline-primary btn-sm"
              v-b-modal.delete-temp-modal
              @click="deleteTemp(row.item)">
              Delete
            </button>
            </div>
            </td>
          </tr>
      </template>
      </v-data-table>
    </div>
</div>
<div v-else>
</div>
<b-modal ref="addTempModal"
  hide-backdrop
  hide-header-close
  content-class="shadow"
  id="addtemp-modal"
  title="Add a Temperature"
  hide-footer>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-group id="form-temp-group"
      label="Temperature:"
      label-for="form-temp-input">
    <b-form-input id="form-temp-input"
      type="text"
      v-model="addTempForm.temp"
      required
      placeholder="Enter temperature here">
    </b-form-input>
    </b-form-group>
    <br>
    <div style="text-align:center">
    <b-button-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset">Cancel</b-button>
    </b-button-group>
    </div>
    </b-form>
</b-modal>
<b-modal ref="editUserModal"
  hide-backdrop
  hide-header-close
  content-class="shadow"
  id="edit-user-modal"
  title="Edit User"
  hide-footer>
  <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
    <input id="form-id-edit-input"
      type="hidden"
      v-model="editForm.id"
      required
      placeholder="Enter id here">
    <b-form-group id="form-name-edit-group"
      label="Name:"
      label-for="form-name-edit-input">
      <b-form-input id="form-name-edit-input"
        type="text"
        v-model="editForm.Name"
        required
        placeholder="Enter name here">
      </b-form-input>
    </b-form-group>
    <br>
    <b-form-group id="form-rfid-edit-group"
      label="RFID:"
      label-for="form-rfid-edit-input">
      <b-form-input id="form-rfid-edit-input"
        type="text"
        v-model="editForm.RFID"
        required
        placeholder="Enter RFID here">
      </b-form-input>
    </b-form-group>
    <br>
    <b-form-group id="form-barcode-edit-group"
      label="Barcode:"
      label-for="form-barcode-edit-input">
      <b-form-input id="form-barcode-edit-input"
        type="text"
        v-model="editForm.Barcode"
        required
        placeholder="Enter barcode here">
      </b-form-input>
    </b-form-group>
    <br>
    <div style="text-align:center">
    <b-button-group>
      <b-button type="submit" variant="primary">Update</b-button>
      <b-button type="reset">Cancel</b-button>
    </b-button-group>
    </div>
  </b-form>
</b-modal>
<b-modal ref="editTempModal"
  hide-backdrop
  hide-header-close
  content-class="shadow"
  id="edit-temp-modal"
  title="Edit Temperature"
  hide-footer>
  <b-form @submit="onSubmitTempUpdate" @reset="onResetUpdate2" class="w-100">
      <input id="form-id-edit-input"
        type="hidden"
        v-model="editTempForm.id"
        required
        placeholder="Enter id here">
      <b-form-group id="form-temp-edit-group"
        label="Temperature:"
        label-for="form-temp-edit-input">
        <b-form-input id="form-temp-edit-input"
          type="text"
          v-model="editTempForm.Temperature"
          required
          placeholder="Enter temperature here">
        </b-form-input>
      </b-form-group><br>
      <div style="text-align:center">
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset">Cancel</b-button>
        </b-button-group>
      </div>
  </b-form>
</b-modal>
<b-modal ref="deleteTempModal"
  hide-backdrop
  hide-header-close
  content-class="shadow"
  id="delete-temp-modal"
  title="Delete Temperature"
  hide-footer>
  <b-form @submit="onSubmitTempDelete" class="w-100">
    <input id="form-id-delettemp-input"
      type="hidden"
      v-model="deleteTempForm.id"
      required
      placeholder="Enter id here">
      <div style="text-align:center">
        <strong>Are you sure you want to delete this temperature?</strong><br><br>
        <b-button-group>
          <b-button type="submit" variant="primary">Delete</b-button>
          <b-button block @click="$bvModal.hide('delete-temp-modal')">Close</b-button>
        </b-button-group>
      </div>
  </b-form>
</b-modal>
</div>
</template>

<script>
import router from '../router';
import axios from 'axios';
import BarGraph from '@/components/BarGraph.vue';

export default {
  name: 'Profile',
  components: {
    BarGraph,
  },
  data() {
    return {
      dismissSecs: 10,
      dismissCountDown: 0,
      showDismissibleAlert: false,
      timeout: 5000,
      filter: '',
      id: 0,
      user: [],
      message: '',
      bargraphdata: [],
      bargraphseries: [],
      addTempForm: {
        temp: '',
      },
      editForm: {
        ID: '',
        Name: '',
        RFID: '',
        Barcode: '',
      },
      editTempForm: {
        id: '',
        DateTime: '',
        Temperature: '',
      },
      deleteTempForm: {
        id: '',
      },
      fields: [
        {
          value: 'fever',
          text: 'Fever',
          sortable: false,
        },
        {
          value: 'DateTime',
          text: 'Date/Time',
          sortable: true,
        },
        {
          value: 'Temperature',
          text: 'Temperature',
          sortable: true,
        },
        {
          value: 'controls',
          text: 'Options',
          sortable: false,
        },
      ],
    };
  },
  created() {
    this.id = this.$route.params.id;
    this.getUser(this.id);
  },
  methods: {
    navigate() {
      router.go(-1);
    },
    getUser(id) {
      const http = 'http://';
      const url = location.hostname;
      const portpage = ':5000/profile_data/';
      const path = http.concat(url, portpage, id);
      axios.get(path)
        .then((res) => {
          this.user = res.data;
          this.bargraphdata = this.user.Chart_Temperatures;
          this.bargraphseries = [
            {
              name: 'Temperature',
              data: [this.bargraphdata[13], this.bargraphdata[12], this.bargraphdata[11],
              this.bargraphdata[10], this.bargraphdata[9], this.bargraphdata[8],
              this.bargraphdata[7], this.bargraphdata[6], this.bargraphdata[5],
              this.bargraphdata[4], this.bargraphdata[3], this.bargraphdata[2],
              this.bargraphdata[1], this.bargraphdata[0]],
            },
          ];
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addTemp(payload) {
      const http = 'http://';
      const url = location.hostname;
      const portpage = ':5000/add_temp';
      const path = http.concat(url, portpage);
      axios.post(path, payload)
        .then((res) => {
          const call_response = res.data;
          if (call_response.Success) {
            this.getUser(this.id);
            this.message = 'Temperature added!';
            this.showDismissibleAlert = true;
          } else {
            this.getUser(this.id);
            this.message = call_response.Error;
            this.showDismissibleAlert = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    initForm() {
      this.addTempForm.temp = '';
      this.editForm.ID = '';
      this.editForm.Name = '';
      this.editForm.RFID = '';
      this.editForm.Barcode = '';
      this.editTempForm.id = '';
      this.editTempForm.DateTime = '';
      this.editTempForm.Temperature = '';
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTempModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editUserModal.hide();
      this.initForm();
      this.getUser(this.id);
    },
    onResetUpdate2(evt) {
      evt.preventDefault();
      this.$refs.editTempModal.hide();
      this.initForm();
      this.getUser(this.id);
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addTempModal.hide();
      const payload = {
        temp: this.addTempForm.temp,
        id: this.id,
      };
      this.addTemp(payload);
      this.initForm();
    },
    editUser(user) {
      this.editForm = user;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editUserModal.hide();
      const payload = {
        id: this.editForm.ID,
        name: this.editForm.Name,
        rfid: this.editForm.RFID,
        barcode: this.editForm.Barcode,
      };
      this.updateUser(payload, this.editForm.ID);
    },
    updateUser(payload, userID) {
      const http = 'http://';
      const url = location.hostname;
      const portpage = ':5000/edit_user';
      const path = http.concat(url, portpage);
      axios.post(path, payload)
        .then((res) => {
          const call_response = res.data;
          if (call_response.Success) {
            this.getUser(userID);
            this.message = 'User updated!';
            this.showDismissibleAlert = true;
          } else {
            this.getUser(userID);
            this.message = call_response.Errors;
            this.showDismissibleAlert = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUser(userID);
        });
    },
    editTemp(temp) {
      this.editTempForm = temp;
    },
    onSubmitTempUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTempModal.hide();
      const payload = {
        id: this.editTempForm.id,
        temp: this.editTempForm.Temperature,
      };
      this.updateTemp(payload, this.editTempForm.id, this.id);
    },
    updateTemp(payload, tempID, userID) {
      const http = 'http://';
      const url = location.hostname;
      const portpage = ':5000/edit_temp';
      const path = http.concat(url, portpage);
      axios.post(path, payload)
        .then((res) => {
          const call_response = res.data;
          if (call_response.Success) {
            this.getUser(userID);
            this.message = 'Temperature updated!';
            this.showDismissibleAlert = true;
          } else {
            this.getUser(userID);
            this.message = call_response.Error;
            this.showDismissibleAlert = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUser(userID);
        });
    },
    deleteTemp(temp) {
      this.deleteTempForm = temp;
    },
    onSubmitTempDelete(evt) {
      evt.preventDefault();
      this.$refs.deleteTempModal.hide();
      const payload = {
        id: this.deleteTempForm.id,
      };
      this.removeTemp(payload, this.deleteTempForm.id, this.id);
    },
    removeTemp(payload, tempID, userID) {
      const http = 'http://';
      const url = location.hostname;
      const portpage = ':5000/delete_temp';
      const path = http.concat(url, portpage);
      axios.post(path, payload)
        .then(() => {
          this.getUser(userID);
          this.message = 'Temperature deleted!';
          this.showDismissibleAlert = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUser(userID);
        });
    },
  },
  computed: {
    filteredRows() {
      return this.user.All_Temperatures.filter(temp => {
        const datetime = temp.DateTime.toString().toLowerCase();
        const temperature = temp.Temperature.toString().toLowerCase();
        const searchTerm = this.filter.toLowerCase();

        return datetime.includes(searchTerm)
          || temperature.includes(searchTerm);
      });
    },
    rows() {
      return this.filteredRows.length;
    },
  },
};
</script>

<style>
#close_btn{
  position: absolute;
  right: 6px;
  top: 12px;
}
</style>
