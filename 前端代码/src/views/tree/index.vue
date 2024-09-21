<template>
  <el-row>
    <el-col :span="12">
      <div class="grid-content bg-purple">
        <table1>数据列表</table1>
      </div>
    </el-col>
    <el-col :span="12"><div class="grid-content bg-purple-light">
      <div>
        <table2></table2>
      </div>
      <div>
        <table3></table3>
      </div>

      <div>
        <table4></table4>
      </div>
    </div></el-col>
  </el-row>
<!--  <div>-->
<!--    <div>-->
<!--      <table1>数据列表</table1>-->
<!--    </div>-->
<!--    <div>-->
<!--      <table2></table2>-->
<!--    </div>-->
<!--    <div>-->
<!--      <table3></table3>-->
<!--    </div>-->
<!--    <div>-->
<!--      <table4></table4>-->
<!--    </div>-->
<!--  </div>-->
</template>
<script>
import table1 from './components/table1_test.vue'
import table2 from './components/table2_test.vue'
import table3 from './components/table3_test.vue'
import table4 from './components/table4_test.vue'

export default {
  components: {
    table1,
    table2,
    table3,
    table4
  },
  methods: {
    showDetail(rowData) {
      this.selectedDetailData = rowData.detailColumnData;
    }
  }
}
</script>
<style>
.container {
  display: flex;
}
.component-wrapper {
  flex: 1;
  margin-right: 10px; /* 可选的间距 */
}
.centered-text {
  text-align: center;
}

</style>
