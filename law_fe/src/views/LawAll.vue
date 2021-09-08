<style scoped>
  .char-1{
    font-size: 1em;
  }
  .char-2{
    padding-left: 3em;
  }
  .char-3{
    padding-left: 6em;
  }
  .ac008 {
    background-color:#C00;border-radius:5px;padding:3px;color:white;
  }
  .tqe_header{
    background-color: #057B7B;
  }
  .btn-tqe{
    background-color: #004b4b;
    color:#FFF;
    font-weight: bold;
    margin-top:-4px;
  }
  .txt-tqe{
    font-size: 16px;
    height: 100%;
  }
  .law-title{
    background-color: #f5fcfb;
    border: 1px solid #148383;
    border-left-width: 6px;
    box-shadow: 3px 3px 0px #e8f3f1;
    padding: 10px;
    margin-bottom: 30px;
  }
  .law-reg{
    background-color: #f9fbfb;
    border: 1px solid #bad5d5;
    box-shadow: 3px 3px 0px #e7eeee;
  }
  .fs-5{
    font-size: 18px;
  }
  .fs-4{
    font-size: 22px;
  }
  .fs-3{
    font-size: 24px;
  }
</style>
<template>
  <div class="lawall">
    <div class="container-fluid pt-4 pb-4 tqe_header">
    <div style="height:38px;">
      <input type="text" name="txtkw" id="txtkw" class="txt-tqe" size="50" placeholder="請輸入關鍵字" v-model.trim="txtkw" @keyup.enter="search_query()" />
      <input type="button" name="btnQuery" id="btnQuery" value="  查詢  " class="btn btn-tqe" style="height:100%" v-on:click="search_query()" />
    </div>
    </div>
    <div class="container mt-3" v-if="TYPE == 'head'">
      <div class="text-left fs-3">
        所有條文
      </div>
      <div class="card mb-3 law-title">
        <div class="card-body">
          <div class="row">
            <div class="col col-md-2 text-right">法規名稱：</div>
            <div class="col text-left">{{AA004}}</div>
          </div>
          <div class="row">
            <div class="col col-md-2 text-right">修正(公布)日期：</div>
            <div class="col text-left">{{format_date(AA007)}}</div>
          </div>
          <div class="row" v-if="AA009.length>0">
            <div class="col col-md-2 text-right">生效狀態：</div>
            <div class="col text-left text-danger">
              <span v-if="AA008.length>0">※本法規部分或全部條文尚未生效，最後生效日期：{{format_date(AA008)}}</span>
              <pre class="fs-6">{{AA009}}</pre>
            </div>
          </div>
          <div class="row">
            <div class="col col-md-2 text-right">法規類別：</div>
            <div class="col text-left">{{AA006}}</div>
          </div>
        </div>
      </div>
      <b-card class="mb-4 law-reg">
          <b-card-text v-for="(item,key) in results" :key="key">
            <div class="row mb-2" :class="setChapterClass(item.AB005)" v-if="item.AB005.length>0">
              <div class="col text-left fs-4">
              {{item.AB005}}&nbsp;&nbsp;
              </div>
            </div>
            <div class="row">
              <div class="col col-2 text-right fs-5">{{item.AC010}}</div>
              <div class="col text-left fs-5"><pre>{{item.AC011}}</pre></div>
            </div>
          </b-card-text>
      </b-card>
    </div>
    <div class="container mt-3" v-else-if="TYPE == 'body'">
      <div class="text-left fs-3">
        條文檢索結果
      </div>
      <div class="card mb-4 law-title">
        <div class="card-body">
          <div class="row">
            <div class="col col-md-2 text-right">法規名稱：</div>
            <div class="col text-left">{{AA004}}</div>
          </div>
          <div class="row">
            <div class="col col-md-2 text-right">修正(公布)日期：</div>
            <div class="col text-left">{{format_date(AA007)}}</div>
          </div>
          <div class="row" v-if="AA009.length>0">
            <div class="col col-md-2 text-right">生效狀態：</div>
            <div class="col text-left">{{AA009}}</div>
          </div>
          <div class="row">
            <div class="col col-md-2 text-right">法規類別：</div>
            <div class="col text-left">{{AA006}}</div>
          </div>
        </div>
      </div>
      <div class="card mb-4 law-reg">
        <div class="card-body">
          <div class="row mb-3" v-for="(item,key) in results" :key="key" >
            <div class="col text-right col-2 fs-5">
              {{item.AC010}}
            </div>
            <div class="col text-left fs-5"><pre v-html="replace_key_word(item.AC011)">{{item.AC011}}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  <loading :active.sync="isLoading"></loading>
  </div>
</template>

<script>
import axios from 'axios'
import GLOBAL from '../api/config'
export default {
  name: 'LawAll',
  data () {
    return {
      txtkw: '',
      isLoading: false,
      results: [],
      baseURL: GLOBAL.baseURL,
      TYPE: '',
      AA002: '',
      AA004: '',
      AA006: '',
      AA007: '',
      AA008: '',
      AA009: '',
      AA015: ''
    }
  },
  methods: {
    setChapterClass (AB005) {
      if (AB005.includes('章')) {
        return 'char-2'
      } else if (AB005.includes('節')) {
        return 'char-3'
      }
    },
    search_query () {
      const self = this
      this.$router.push({ name: 'Home', query: { kw: self.txtkw } })
    },
    query_head () {
      const self = this
      axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: 'law_aa_query', AA002: this.$route.params.AA002 } }).then(function (response) {
        const res = response.data
        self.AA004 = res[0].AA004
        self.AA006 = res[0].AA006
        self.AA007 = res[0].AA007
        self.AA008 = res[0].AA008
        self.AA009 = res[0].AA009
      })
    },
    query_detail () {
      const self = this
      if (self.$route.params.TYPE === 'head') {
        const apiName = 'law_ac_query_all'
        axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: apiName, AA002: self.AA002, AC011: self.$route.params.kw } }).then(function (response) {
          console.log(response.data)
          self.results = response.data
          setTimeout(() => {
            self.isLoading = false
          }, 500)
        })
      } else if (self.$route.params.TYPE === 'body') {
        const apiName = 'law_ac_query_single'
        axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: apiName, AA002: self.AA002, AC011: self.$route.params.kw } }).then(function (response) {
          console.log(response.data)
          self.results = response.data
          setTimeout(() => {
            self.isLoading = false
          }, 500)
        })
      }
    },
    format_date (d) {
      const tempDate = d - 19110000
      let year = null
      let month = null
      let day = null
      if ((tempDate).toString().length === 7) {
        year = tempDate.toString().slice(0, 3)
        month = tempDate.toString().slice(3, 5)
        day = tempDate.toString().slice(5, 7)
      } else {
        year = tempDate.toString().slice(0, 2)
        month = tempDate.toString().slice(2, 4)
        day = tempDate.toString().slice(4, 6)
      }
      return `民國 ${year} 年 ${month} 月 ${day} 日 `
    },
    replace_key_word (w) {
      const reg = new RegExp(this.txtkw, 'g')
      return w.replace(reg, `<span style="color: red;">${this.txtkw}</span>`)
    }
  },
  mounted () {
    const self = this
    self.AA002 = self.$route.params.AA002
    self.txtkw = self.$route.params.kw
    self.TYPE = self.$route.params.TYPE
    self.isLoading = true
    self.query_head()
    self.query_detail()
  }
}

</script>
