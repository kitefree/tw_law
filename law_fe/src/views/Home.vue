<style scoped>
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
</style>
<template>
  <div class="home">
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

    <div class="container-md mt-3">
      <div class="accordion" role="tablist" v-show="AA_rows>0 || AC_rows>0">
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button block v-b-toggle.accordion-1 variant="lighty text-left">中央法規 > 法規名稱&nbsp;<span class="badge rounded-pill bg-primary" style="color:white">{{AA_results.length}}</span></b-button>
          </b-card-header>
          <b-collapse id="accordion-1" accordion="my-accordion" role="tabpanel">
            <b-card-body>
              <b-card-text  v-show="AA_rows>0">
              <b-table id="table1" striped hover :items="AA_results" :fields="AA_fields" :per-page="perPage" :current-page="AA_currentPage">
              <!-- A virtual column -->
              <template #cell(index)="data">
              {{(AA_currentPage-1)*perPage + data.index + 1 }}
              </template>
              <!-- A virtual composite column -->
              <template #cell(content)="data" label-align="left">
                <a href="javascript:void(0)" class="text-decoration-none"  @click="query_detail(data.item.AA002,data.item.TYPE)">
                  <span v-html="replace_key_word(data.item.AA004)"></span> ({{format_date(data.item.AA007)}})
                </a>
              </template>
              </b-table>
              </b-card-text>
            </b-card-body>
              <b-pagination  v-show="AA_rows>0"
                v-model="AA_currentPage"
                :total-rows="AA_rows"
                :per-page="perPage"
                aria-controls="table1"
                align="center"
              ></b-pagination>
          </b-collapse>
        </b-card>

        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button block v-b-toggle.accordion-2 variant="light text-left">
            中央法規 > 法條內容&nbsp;<span class="badge rounded-pill text-left bg-primary" style="color:white">{{AC_results.length}}</span>
            </b-button>
          </b-card-header>
          <b-collapse id="accordion-2" accordion="my-accordion" role="tabpanel">
            <b-card-body>
              <b-card-text v-show="AC_rows>0">
              <b-table id="table2" striped hover :items="AC_results" :fields="AC_fields" :per-page="perPage" :current-page="AC_currentPage">
              <!-- A virtual column -->
              <template #cell(index)="data">
              {{(AC_currentPage-1)*perPage + data.index + 1 }}
              </template>
              <!-- A virtual composite column -->
              <template #cell(content)="data" label-align="left">
              <a href="javascript:void(0)" class="text-decoration-none text-left"  @click="query_detail(data.item.AC003,data.item.TYPE)">
                <span class="ac008" v-if="data.item.AC008=='廢'">{{data.item.AC008}}</span>
                {{data.item.AC006}} ({{format_date(data.item.AC007)}})
              </a>
              </template>
              </b-table>
              </b-card-text>
            </b-card-body>
              <b-pagination v-show="AC_rows>0"
                v-model="AC_currentPage"
                :total-rows="AC_rows"
                :per-page="perPage"
                aria-controls="table2"
                align="center"
              ></b-pagination>
          </b-collapse>
        </b-card>

      </div>
    </div>
    <b-toast id="my-toast" variant="warning" solid>
      <template #toast-title>
        <div class="d-flex flex-grow-1 align-items-baseline">
          <b-img blank blank-color="#ff5555" class="mr-2" width="12" height="12"></b-img>
          <strong class="mr-auto">提示!</strong>
          <!-- <small class="text-muted mr-2">42 seconds ago</small> -->
        </div>
      </template>
      {{text_tips}}
    </b-toast>
    <loading :active.sync="isLoading"></loading>
  </div>
</template>

<script>
import GLOBAL from '../api/config'
// @ is an alias to /src
import axios from 'axios'

export default {
  name: 'Home',
  data () {
    return {
      // isOpen: '',
      // kw_results: [],
      // isClickList: false,
      txtkw: '',
      text_tips: '',
      perPage: 10,
      AC_currentPage: 1,
      AA_currentPage: 1,
      AC_rows: 0,
      AA_rows: 0,
      isLoading: false,
      baseURL: GLOBAL.baseURL,
      AA_results: [],
      AC_results: [],
      AA_fields: [
        // A virtual column that doesn't exist in items
        { key: 'index', label: '代號' },
        { key: 'content', label: '法規名稱', tdClass: 'text-left' }
      ],
      AC_fields: [
        // A virtual column that doesn't exist in items
        { key: 'index', label: '代號' },
        { key: 'content', label: '法規名稱', tdClass: 'text-left' }
      ]
    }
  },
  // watch: {
  //   txtkw () {
  //     const self = this
  //     if (self.txtkw.length === 0) {
  //       self.kw_results = []
  //       return
  //     }
  //     if (this.txtkw.length < 2) {
  //       return
  //     }
  //     if (self.isClickList === false) {
  //       self.isLoading = true
  //       axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: 'search_autoComplete', txtkw: self.txtkw } }).then(function (response) {
  //         setTimeout(() => {
  //           self.isLoading = false
  //           if (response.data !== undefined) {
  //             self.kw_results = response.data
  //             self.isOpen = true
  //           } else {
  //             self.kw_results = []
  //             self.isOpen = false
  //           }
  //         }, 300)
  //       })
  //     } else if (self.isClickList === true) {
  //       self.search_query()
  //     }

  //     self.isClickList = false
  //   }
  // },
  methods: {
    // show_kw_list () {
    //   const self = this
    //   // self.kw_results = self.datas.filter(function (item, index, array) {
    //   //   return item.toLowerCase().indexOf(self.txtkw.toLowerCase()) > -1
    //   // })
    //   this.isOpen = self.kw_results.length > 0
    // },
    // select_list (result) {
    //   const self = this
    //   self.txtkw = result
    //   self.isOpen = false
    //   self.isClickList = true
    // },
    search_query () {
      const self = this
      if (self.txtkw.length === 0) {
        self.text_tips = '請輸入關鍵字'
        self.$bvToast.show('my-toast')
        return
      }

      if (self.txtkw.length < 2) {
        self.text_tips = '請輸入2個字以上的關鍵字'
        self.$bvToast.show('my-toast')
        return
      }
      self.isLoading = true
      self.AA_results = []
      self.AC_results = []
      self.AA_rows = 0
      self.AC_rows = 0
      self.AA_currentPage = 1
      self.AC_currentPage = 1
      axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: 'search_query_AA', txtkw: self.txtkw } }).then(function (response) {
        console.log(response.data)
        self.AA_results = response.data
        self.AA_rows = self.AA_results.length
        return axios.get(`${GLOBAL.baseURL}/api.php`, { params: { api: 'search_query_AC', txtkw: self.txtkw } })
      }).then(function (response) {
        console.log(response.data)
        self.AC_results = response.data
        self.AC_rows = self.AC_results.length
        setTimeout(() => {
          self.isLoading = false
        }, 200)
      })
    },
    query_detail (AC003, TYPE) {
      const self = this
      self.isLoading = true
      this.$router.push({ name: 'LawAll', params: { AA002: AC003, kw: self.txtkw, TYPE: TYPE } })
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
    if (self.$route.query.kw === undefined) return
    self.txtkw = self.$route.query.kw
    self.search_query()
  }
}
</script>
