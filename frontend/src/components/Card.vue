<template>
  <el-card>
    <el-image :src="item.face" />
    <span class="info">
      <span class="uname">{{item.uname}}</span>
      <br />
      <el-link type="primary" class="room" icon="el-icon-video-play" href='`https://live.bilibili.com/${item.room_id}`'>进入直播间</el-link>
    </span>
    <a class="show el-icon-view"></a>
  </el-card>
</template>

<script>
export default {
  name: "Card",
  data() {
    return {};
  },
  props: ["item"],
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-card {
  height: 120px;
  margin-top: 15px;
  padding: 15px;
}
.el-card >>> .el-card__body {
  display: flex;
  align-items: center;
  padding: 0;
  height: 100%;
  position: relative;
}
.el-card .el-image {
  height: 100%;
}
.el-card .info {
  margin-left: 15px;
}
.el-card .uname {
  font-size: 28px;
  font-weight: bold;
  color: #606266;
}
.el-card .show {
  font-size: 28px;
  cursor: pointer;
  position: absolute;
  right: 15px;
}
</style>