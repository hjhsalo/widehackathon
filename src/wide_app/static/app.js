var app = new Vue({
    el: '#app',
    // delimiters: ['${', '}'],
    data () {
        return {
            keywords: [],
            searchResults: [],
            annifSources: [],
            datasetSources: [],
            publishedStartDate: null,
            publishedEtartDate: null,
            showKeywords: false,
            showSearchResults: false,
            hello: 'hellllo'
        }
    },
    methods: {
        scrape: function(tabs) {
            console.log('SCRAPING !');
            console.log(this.keywords);
            var vm = this;
            vm.showKeywords = false;
            vm.showSearchResults = false;
            this.$http.post('/scrape', { content: document.body.innerHTML }).then(response => {
                console.log('scrape ok');
                console.log(response);
                vm.keywords = response.body.keywords;
                vm.showKeywords = true;
            }, response => {
                console.log('fffffffffff');
                console.log(response);
            });


        },

        searchDatasets: function(tabs) {
            // search request wouldn't normally require involvement from the tab content script,
            // but for some reason http requests do not work from the background script.......
            console.log('searching datasets...');
            var vm = this;
            this.$http.post('/search', { content: vm.keywords }).then(response => {
                console.log('search ok');
                console.log(response);
                vm.searchResults = response.body.results;
                vm.showSearchResults = true;
            }, response => {
                console.log('fffffffffff');
                console.log(response);
            });
        },

        listenForClicks: function() {
            document.addEventListener("click", (e) => {
                if (e.target.classList.contains("scrape")) {
                    this.scrape();
                }
                else if (e.target.classList.contains("search")) {
                    this.searchDatasets();
                }
            });
        },

        reportExecuteScriptError: function(error) {
            document.querySelector("#error-content").classList.remove("hidden");
            console.error(`Failed to execute beastify content script: ${error.message}`);
        }
    },
    created () { 
        console.log('app created()...');
        this.listenForClicks();
    }
})