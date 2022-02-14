<template>
<div>
<b-navbar toggleable="lg" type="dark" variant="dark">
<b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
<b-collapse id="nav-collapse" is-nav>
  <b-navbar-nav>
    <b-nav-item href="#"><button type="button" class="btn btn-primary"
      v-b-modal.adduser-modal>
      Add User</button>
    </b-nav-item>
    <b-nav-item href="#"><button type="button" class="btn btn-primary"
      v-b-modal.uploadfile-modal>
      Upload File</button>
    </b-nav-item>
  </b-navbar-nav>

  <!-- Right aligned nav items -->
  <b-navbar-nav class="ml-auto">
  <b-nav-form>
    <input type="text"
      placeholder="Search the database"
      v-model="filter" />
  </b-nav-form>
  </b-navbar-nav>
</b-collapse>
</b-navbar>
<b-alert v-model="showUploadMessage" variant="success" dismissible>
  {{ uploadmessage }}
</b-alert>
<b-alert v-model="showUploadErrors" variant="danger" dismissible>
  <div v-for="error in uploaderrors">{{ error }}<br>
  </div>
</b-alert>
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
<v-data-table
  :headers="fields"
  :items="filteredRows"
  :items-per-page="15"
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
      <td>{{row.item.Name}}</td>
      <td>{{row.item.RFID}}</td>
      <td>{{row.item.Barcode}}</td>
      <td>
        <div class="btn-group" role="group" aria-label="First group">
          <button
            type="button"
            class="btn btn-outline-primary btn-sm"
            v-b-modal.edit-user-modal
            @click="editUser(row.item)">
            Edit
          </button>
          <button
            type="button"
            class="btn btn-outline-primary btn-sm"
            v-b-modal.delete-user-modal
            @click="deleteUser(row.item)">
            Delete
          </button>
        </div>
      </td>
      <td><router-link :to="{ name: 'Profile', params: { id: row.item.id } }">
        View Profile</router-link></td>
    </tr>
  </template>
</v-data-table>
<b-modal ref="addUserModal"
  hide-backdrop
  hide-header-close
  content-class="shadow"
  id="adduser-modal"
  title="Add a New User"
  hide-footer>
  <b-form @submit="onSubmit" @reset="onReset" class="w-100">
  <b-form-group id="form-name-group"
    label="Name:"
    label-for="form-name-input">
    <b-form-input id="form-name-input"
      type="text"
      v-model="addUserForm.name"
      required
      placeholder="Enter name here">
    </b-form-input>
  </b-form-group>
  <br>
  <b-form-group id="form-rfid-group"
    label="RFID:"
    label-for="form-rfid-input">
    <b-form-input id="form-rfid-input"
      type="text"
      v-model="addUserForm.rfid"
      required
      placeholder="Enter RFID here">
    </b-form-input>
  </b-form-group>
  <br>
  <b-form-group id="form-barcode-group"
    label="Barcode:"
    label-for="form-barcode-input">
    <b-form-input id="form-barcode-input"
      type="text"
      v-model="addUserForm.barcode"
      required
      placeholder="Enter barcode here">
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
<b-modal ref="uploadFileModal"
  hide-backdrop
  hide-header-close
  content-class="shadow"
  id="uploadfile-modal"
  title="Upload a CSV File"
  hide-footer>
  <div align="center">
    <strong>Only the CSV file extension is allowed</strong>
  </div>
  <br>
  <label>File
    <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
  </label>
  <button class="btn btn-primary" v-on:click="submitFile()">Submit</button>
  <b-button block @click="$bvModal.hide('uploadfile-modal')">Close</b-button>
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
    </b-form-group><br>
    <b-form-group id="form-rfid-edit-group"
      label="RFID:"
      label-for="form-rfid-edit-input">
      <b-form-input id="form-rfid-edit-input"
        type="text"
        v-model="editForm.RFID"
        required
        placeholder="Enter RFID here">
      </b-form-input>
    </b-form-group><br>
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
<b-modal ref="deleteUserModal"
  hide-backdrop
  hide-header-close
  content-class="shadow"
  id="delete-user-modal"
  title="Delete User"
  hide-footer>
  <b-form @submit="onSubmitDelete" class="w-100">
      <input id="form-id-edit-input"
        type="hidden"
        v-model="deleteForm.id"
        required
        placeholder="Enter id here">
        <div style="text-align:center">
          <strong>Are you sure you want to delete this user?</strong><br><br>
          <b-button-group>
            <b-button type="submit" variant="primary">Delete</b-button>
            <b-button block @click="$bvModal.hide('delete-user-modal')">Close</b-button>
          </b-button-group>
        </div>
  </b-form>
</b-modal>
</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      dismissSecs: 20,
      dismissCountDown: 0,
      showDismissibleAlert: false,
      timeout: 5000,
      filter: '',
      users: [],
      message: '',
      errormessage: '',
      uploadmessage: '',
      uploaderrors: '',
      showError: false,
      showUploadMessage: false,
      showUploadErrors: false,
      file: '',
      addUserForm: {
        name: '',
        rfid: '',
        barcode: '',
      },
      editForm: {
        id: '',
        Name: '',
        RFID: '',
        Barcode: '',
      },
      deleteForm: {
        id: '',
      },
      fields: [
        {
          value: 'fever',
          text: 'Fever',
          sortable: false,
        },
        {
          value: 'Name',
          text: 'Name',
          sortable: true,
        },
        {
          value: 'RFID',
          text: 'RFID',
          sortable: false,
        },
        {
          value: 'Barcode',
          text: 'Barcode',
          sortable: false,
        },
        {
          value: 'controls',
          text: 'Options',
          sortable: false,
        },
        {
          value: 'profile',
          text: 'Profile',
          sortable: false,
        },
      ],
    };
  },
  components: {
  },
  methods: {
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    },
    submitFile() {
      const formData = new FormData();
      formData.append('file', this.file);
      const http = 'http://';
      const url = location.hostname;
      const portpage = ':5000/upload';
      const path = http.concat(url, portpage);
      axios.post(path,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        },
      ).then((res) => {
        const call_response = res.data;
        if (call_response.Success) {
          this.getUsers();
          this.uploadmessage = 'File uploaded!';
          this.uploaderrors = call_response.Errors;
          this.showUploadMessage = true;
          this.showUploadErrors = true;
          this.$refs.uploadFileModal.hide();
        } else {
          this.getUsers();
          this.errormessage = call_response.Errors;
          this.showDismissibleAlert = true;
          this.$refs.uploadFileModal.hide();
        }
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    getUsers() {
      const http = 'http://';
      const url = location.hostname;
      const portpage = ':5000/get_db';
      const path = http.concat(url, portpage);
      axios.get(path)
        .then((res) => {
          this.users = res.data.users;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addUser(payload) {
      const http = 'http://';
      const url = location.hostname;
      const portpage = ':5000/add_user';
      const path = http.concat(url, portpage);
      axios.post(path, payload)
        .then((res) => {
          const call_response = res.data;
          if (call_response.Success) {
            this.getUsers();
            this.message = 'User added!';
            this.showDismissibleAlert = true;
          } else {
            this.getUsers();
            this.message = call_response.Errors;
            this.showDismissibleAlert = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    initForm() {
      this.addUserForm.name = '';
      this.addUserForm.rfid = '';
      this.addUserForm.barcode = '';
      this.editForm.id = '';
      this.editForm.Name = '';
      this.editForm.RFID = '';
      this.editForm.Barcode = '';
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editUserModal.hide();
      this.initForm();
      this.getUsers();
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      const payload = {
        name: this.addUserForm.name,
        rfid: this.addUserForm.rfid,
        barcode: this.addUserForm.barcode,
      };
      this.addUser(payload);
      this.initForm();
    },
    editUser(user) {
      this.editForm = user;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editUserModal.hide();
      const payload = {
        id: this.editForm.id,
        name: this.editForm.Name,
        rfid: this.editForm.RFID,
        barcode: this.editForm.Barcode,
      };
      this.updateUser(payload);
    },
    updateUser(payload) {
      const http = 'http://';
      const url = location.hostname;
      const portpage = ':5000/edit_user';
      const path = http.concat(url, portpage);
      axios.post(path, payload)
        .then((res) => {
          const call_response = res.data
          if (call_response.Success) {
            this.getUsers();
            this.message = 'User updated!';
            this.showDismissibleAlert = true;
          } else {
            this.getUsers();
            this.message = call_response.Errors;
            this.showDismissibleAlert = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUsers();
        });
    },
    deleteUser(user) {
      this.deleteForm = user;
    },
    onSubmitDelete(evt) {
      evt.preventDefault();
      this.$refs.deleteUserModal.hide();
      const payload = {
        id: this.deleteForm.id,
      };
      this.removeUser(payload);
    },
    removeUser(payload) {
      const http = 'http://';
      const url = location.hostname;
      const portpage = ':5000/delete_user';
      const path = http.concat(url, portpage);
      axios.post(path, payload)
        .then(() => {
          this.getUsers();
          this.message = 'User deleted!';
          this.showDismissibleAlert = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUsers();
        });
    },
  },
  computed: {
    filteredRows() {
      return this.users.filter(user => {
        const name = user.Name.toLowerCase();
        const rfid = user.RFID.toString().toLowerCase();
        const barcode = user.Barcode.toString().toLowerCase();
        const searchTerm = this.filter.toLowerCase();

        return name.includes(searchTerm)
          || rfid.includes(searchTerm)
          || barcode.includes(searchTerm);
      });
    },
  },
  created() {
    this.getUsers();
  },
};
</script>

<style>
a:link { color: black; }
a​:active { color: black; }
a​:visited { color: black; }
a​:hover { color: white; }

input[type=text] {
  background-color: #FFFFFF;
  color: black;
  border: 2px solid #C6C6C6;
  border-radius: 4px;
  padding: 7px 12px;
  margin: 4px 0;
}
</style>
