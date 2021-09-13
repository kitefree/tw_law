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
  .char-4{
    padding-left: 9em;
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
  .btn-second-tqe{
    background-color: #148383;
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
      <div class="row" style="justify-content:center">
        <div class="col-10">
          <input type="text" name="txtkw" id="txtkw" class="txt-tqe w-25" placeholder="請輸入關鍵字" v-model.trim="txtkw" @keyup.enter="search_query()" />
          <input type="button" name="btnQuery" id="btnQuery" value="  查詢  " class="btn btn-tqe" style="height:100%" v-on:click="search_query()" />
        </div>
      </div>
      <!-- <div class="row" style="justify-content:center">
        <div class="col-3">
        <ul v-show="isOpen" class="list-group mb-3" style="margin-left:-12px">
            <li v-for="(result, i) in kw_results" :key="i" class="list-group-item text-left" style="z-index:99" @click="select_list(result.AA004)">
                {{ result.AA004 }}
            </li>
        </ul>
        </div>
      </div> -->
    </div>
    </div>
    <!-- 所有條文 -->
    <div class="container mt-3" v-if="SEARCH_TYPE == '法規名稱'">
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
        <div class="row">
          <div class="col">
          <b-button variant="btn btn-second-tqe mr-4" @click="query_law_ac()">所有條文</b-button>
          <b-button variant="btn btn-second-tqe mr-4" @click="query_law_ab()" v-if="AB_COUNT >0">編章節</b-button>
          </div>
        </div>
      </div>
      <!-- 底部身資料 預設 -->
      <b-card class="mb-4 law-reg" v-if="OP_TYPE == '所有條文'">
          <b-card-text v-for="(item,key) in results" :key="key">
            <div class="row mb-1" :class="setChapterClass(item.AB005)" v-if="item.AB005.length>0">
              <div class="col text-left fs-4" style="font-weight:bold">
              {{item.AB005}}&nbsp;&nbsp;
              </div>
            </div>
            <div class="row" v-if="item.AC010 != undefined && item.AC010 != ''">
              <div class="col col-2 text-right fs-5">{{item.AC010}}</div>
              <div class="col text-left fs-5"><pre>{{item.AC011}}</pre></div>
            </div>
          </b-card-text>
      </b-card>
      <!-- 底部身資料 點選編章節 -->
      <b-card class="mb-4 law-reg" v-if="OP_TYPE == '編章節'">
          <!-- <a :href="'https://law.moj.gov.tw/LawClass/LawAllPara.aspx?pcode=' + this.$route.params.AA002" target="_blank">官網</a> -->
          <b-card-text v-for="(item,key) in AB_LIST" :key="key">
            <div class="row ml-4">
              <div class="col text-left fs-4">
              <pre><b-link href="javascript:void(0)" style="text-decoration:none" @click="query_detail_by_AB003(item.AB003)">{{item.AB005}} § {{item.numStart}}</b-link></pre>
              </div>
            </div>
          </b-card-text>
      </b-card>
      <!-- 底部身資料 點選編章節編號 -->
      <b-card class="mb-4 law-reg" v-if="OP_TYPE == '編章節編號'">
          <b-card-text v-for="(item,key) in results" :key="key">
            <div class="row mb-1" :class="setChapterClass(item.AB005)" v-if="item.AB005.length>0">
              <div class="col text-left fs-4" style="font-weight:bold">
              {{item.AB005}}&nbsp;&nbsp;
              </div>
            </div>
            <div class="row" v-if="item.AC010 != undefined && item.AC010 != ''">
              <div class="col col-2 text-right fs-5">{{item.AC010}}</div>
              <div class="col text-left fs-5"><pre>{{item.AC011}}</pre></div>
            </div>
          </b-card-text>
      </b-card>
    </div>
    <!-- 條文檢索結果 -->
    <div class="container mt-3" v-else-if="SEARCH_TYPE == '法條內容'">
      <div class="text-left fs-3">
        條文檢索結果
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
            <div class="col text-left">{{AA009}}</div>
          </div>
          <div class="row">
            <div class="col col-md-2 text-right">法規類別：</div>
            <div class="col text-left">{{AA006}}</div>
          </div>
          <div class="row mt-4">
            <div class="col">
            <b-button variant="btn btn-second-tqe mr-4" @click="query_law_ac()">所有條文</b-button>
            <b-button variant="btn btn-second-tqe mr-4" @click="query_law_ab()" v-if="AB_COUNT >0">編章節</b-button>
            </div>
          </div>
        </div>
      </div>
      <!-- 底部身資料 -->
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
      SEARCH_TYPE: '',
      OP_TYPE: '',
      AB_LIST: [],
      AB_COUNT: 0,
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
      } else if (AB005.includes('款')) {
        return 'char-4'
      }
    },
    search_query () {
      const self = this
      this.$router.push({ name: 'Home', query: { kw: self.txtkw } })
    },
    // 法規單頭查詢
    query_head () {
      const self = this
      axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: 'query_law_aa', AA002: this.$route.params.AA002 } }).then(function (response) {
        const res = response.data
        self.AA004 = res[0].AA004
        self.AA006 = res[0].AA006
        self.AA007 = res[0].AA007
        self.AA008 = res[0].AA008
        self.AA009 = res[0].AA009
      })
    },
    // 點擊編章節按鈕事件
    query_law_ab () {
      const self = this
      if (self.OP_TYPE === '編章節') return
      self.AB_LIST = []
      self.OP_TYPE = '編章節'
      self.isLoading = true
      self.$router.push({ name: 'LawAll', params: { AA002: self.AA002, kw: self.txtkw, SEARCH_TYPE: '法規名稱', OP_TYPE: self.OP_TYPE } })
    },
    // 點擊所有條文按鈕事件
    query_law_ac () {
      const self = this

      if (self.SEARCH_TYPE === '法規名稱' && self.OP_TYPE === '所有條文') {
        return
      }
      // 由法條內容分類串過來的，這時如果再點擊所有條文按鈕，要回到看整篇法規的模式
      if (self.SEARCH_TYPE === '法規名稱') {
        self.isLoading = true
        self.$router.push({ name: 'LawAll', params: { AA002: self.AA002, kw: self.txtkw, SEARCH_TYPE: '法規名稱', OP_TYPE: '所有條文' } })
      } else if (self.SEARCH_TYPE === '法條內容') {
        self.isLoading = true
        self.$router.push({ name: 'LawAll', params: { AA002: self.AA002, kw: self.txtkw, SEARCH_TYPE: '法規名稱', OP_TYPE: '所有條文' } })
      }
      // eslint-disable-next-line no-debugger
      // debugger
    },
    // 點擊編章節 內的法規內容
    query_detail_by_AB003 (AB003) {
      const self = this
      self.OP_TYPE = '所有條文'
      self.isLoading = true
      // query: { kw: self.txtkw }
      self.$router.push({ name: 'LawAll', params: { AA002: self.AA002, kw: self.txtkw, SEARCH_TYPE: '法規名稱', OP_TYPE: '編章節編號', AB003 } })
      // const apiName = 'query_detail_by_AB003'
      // axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: apiName, AA002: self.AA002, AB003 } }).then(function (response) {
      //   console.log(response.data)
      //   self.results = response.data
      //   setTimeout(() => {
      //     self.isLoading = false
      //   }, 500)
      // })
    },
    // 法規單身查詢
    query_detail () {
      const self = this
      self.results = []
      self.isLoading = true
      const apiName2 = 'query_law_ab_count'

      // 確認 法規表 筆數, 使用v-if 方式決定是否show 編章節按鈕
      axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: apiName2, AA002: self.AA002 } }).then(function (response) {
        self.AB_COUNT = response.data[0].cnt
      })

      // [法規名稱]類別點擊進來的
      if (self.$route.params.SEARCH_TYPE === '法規名稱') {
        console.log('OP_TYPE:', self.OP_TYPE)
        console.log('AB003:', self.AB003)

        // 預設查詢所有[法條內容]
        if (self.OP_TYPE === '所有條文') {
          const apiName = 'query_law_ac_all'
          axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: apiName, AA002: self.AA002, AC011: self.$route.params.kw } }).then(function (response) {
            self.results = response.data
            setTimeout(() => {
              self.isLoading = false
              self.isResultDone = true
            }, 200)
          })
        } else if (self.OP_TYPE === '編章節') {
          const apiName = 'query_law_ab'
          axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: apiName, AA002: self.AA002 } }).then(function (response) {
            self.AB_LIST = response.data
            setTimeout(() => {
              self.isLoading = false
              self.isResultDone = true
            }, 200)
          })
        } else if (self.OP_TYPE === '編章節編號') {
          const apiName = 'query_detail_by_AB003'
          axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: apiName, AA002: self.AA002, AB003: self.AB003 } }).then(function (response) {
            console.log(response.data)
            self.results = response.data
            setTimeout(() => {
              self.isLoading = false
            }, 500)
          })
        }
      // [法條內容]類別點擊進來的
      } else if (self.$route.params.SEARCH_TYPE === '法條內容') {
        // 只查含有關鍵字的[法條內容]
        const apiName = 'query_law_ac_single'
        axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: apiName, AA002: self.AA002, AC011: self.$route.params.kw } }).then(function (response) {
          self.results = response.data
          self.isLoading = false
          self.isResultDone = true
        })
      }
    },
    format_date (d) {
      if (d === '99991231') {
        return '未定'
      }
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
    self.AB003 = self.$route.params.AB003
    self.txtkw = self.$route.params.kw
    self.SEARCH_TYPE = self.$route.params.SEARCH_TYPE
    self.OP_TYPE = self.$route.params.OP_TYPE
    self.isLoading = true
    self.query_head()
    self.query_detail()
  }
}

</script>
