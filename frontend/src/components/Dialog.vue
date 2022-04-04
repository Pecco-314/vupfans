<template>
    <el-dialog :visible.sync="id" :title=title :before-close="onClose">
        <el-collapse v-model="activeRoom" accordion v-for="item of currentNameList" :key="item.medal.id">
        <el-collapse-item :name="item.medal.id">
            <template slot="title">
                <el-link v-if="item.medal.id" :href="`https://live.bilibili.com/${item.medal.id}`">{{item.medal.name}}</el-link>
                <el-link disabled v-else>（无粉丝牌）</el-link>
                <span class="cnt-span">{{item.cnt}}</span>
            </template>
            <!-- <el-table stripe>
            </el-table> -->
        </el-collapse>
        <el-pagination layout="prev, pager, next, jumper" :total="fullNameList.length" hide-on-single-page small @current-change="onCurrentPageChange">
        </el-pagination>
    </el-dialog>
</template>

<script>
import axios from "axios";
export default {
  name: "Dialog",
  data() {
    return {
        fullNameList: [],
        activeRoom: '',
        page: 1,
        pageSize: 10,
    };
  },
  computed: {
      currentNameList() {
          return this.fullNameList.slice((this.page - 1) * this.pageSize, this.page * this.pageSize);
      }
  },
  methods: {
      onCurrentPageChange(page) {
          this.page = page;
      },
      onClose(done) {
          this.$emit("hiddenDialog");
          this.fullNameList = [];
          this.activeName = '';
          this.page = 1,
          done();
      }
  },
  watch: {
      id: function(val) {
            if (val) {
                axios.get(`http://124.222.81.160:5000/medalnames?roomid=${val}`)
                    .then(response => { this.fullNameList = response.data; })
                    .catch(error => console.error(error))
            }
      }
  },
  props: [
      "title",
      "id",
    ],
};
</script>

<style scoped>
.cnt-span {
    position: absolute;
    right: 45px;
}

.el-collapse-item .el-link {
    color: #606266!important;
}

.el-pagination {
    margin-top: 15px;
}

</style>