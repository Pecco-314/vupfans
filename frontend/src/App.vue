<template>
  <div id="app">
    <div id="main">
      <el-input v-model="input" placeholder="搜索"></el-input>
      <el-skeleton :rows="6" animated v-show="loading" />
      <div v-for="item in list" :key=item.room_id>
        <Card :item=item>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Card from './components/Card'

export default {
  name: 'App',
  data() {
    return {
      input: '',
      list: [],
      loading: false,
    }
  },
  watch: {
    input: function (val) {
      this.loading = true;
      axios.get(`http://124.222.81.160:5000/room?keyword=${val}`)
           .then(response => { this.list = response.data; this.loading = false; })
           .catch(error => console.error(error))
    }
  },
  components: {
    Card
  },
  metaInfo: {
    title: 'Bilibili直播间粉丝牌成分查询',
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