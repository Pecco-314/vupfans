<template>
  <div id="app">
    <div id="main">
      <el-input v-model="input" placeholder="搜索"></el-input>
      <el-skeleton :rows="6" animated v-show="loading" />
      <div v-for="item in list" :key=item.room_id>
        <Card :item=item @showButtonClicked="showDialog" />
      </div>
      <Dialog :id=dialog.id :title=dialog.title @hiddenDialog=hiddenDialog />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Card from './components/Card'
import Dialog from "./components/Dialog"

export default {
  name: 'App',
  data() {
    return {
      input: '',
      list: [],
      loading: false,
      dialog: {
        id: null,
        title: '',
      }
    }
  },
  watch: {
    input: function (val) {
      this.loading = true;
      this.list = [];
      axios.get(`http://124.222.81.160:5000/room?keyword=${val}`)
           .then(response => { this.list = response.data; this.loading = false; })
           .catch(error => console.error(error))
    }
  },
  methods: {
    showDialog(roomId, uname) {
      this.dialog.id = roomId;
      this.dialog.title = `「${uname}」直播间的粉丝牌分布`
    },
    hiddenDialog() {
      this.dialog.id = null;
    }
  },
  components: {
    Card,
    Dialog,
  },
  metaInfo: {
    meta: [
      { name: 'referrer', content: 'no-referrer' },
    ] 
  }
}
</script>

<style>
#main {
  padding-left: 5vw;
  padding-right: 5vw;
  padding-top: 15px;
}

#main .el-skeleton {
  margin-top: 15px;
}
</style>