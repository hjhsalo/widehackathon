
var text = 'A robot may not injure a human being or, through inaction, allow a human being to come to harm. A robot must obey the orders given it by human beings except where such orders would conflict with the First Law.A robot must protect its own existence as long as such protection does not conflict with the First or Second Laws'

var app = new Vue({
    el: '#app',
    data () {
        return {
            scrapeInput: null,
            keywords: [],
            searchResults: [],
            annifSources: [],
            datasetSources: [],
            publishedStartDate: null,
            publishedEtartDate: null,
            showKeywords: false,
            showSearchResults: false,
            youtubeLink: null,
            showKeywordsLoading: false,
            showSearchLoading: false,
            recursionLevel: 0
        }
    },
    methods: {
        scrape: function(tabs) {
            console.log('SCRAPING !');
            var vm = this;
            vm.showKeywords = false;
            vm.showSearchResults = false;
            if (!vm.scrapeInput) {
                return;
            }
            vm.showKeywordsLoading = true;
            this.$http.post('/scrape', { content: vm.scrapeInput }).then(response => {
                console.log('scrape ok');
                console.log(response);
                keywords = response.body.keywords;
                vm.keywords = []
                for (let kw of keywords) {
                    item = { value: kw, checked: true};
                    vm.keywords.push(item)
                }
                vm.showKeywordsLoading = false;
                vm.showKeywords = true;
            }, response => {
                vm.showKeywordsLoading = false;
                console.log('fffffffffff');
                console.log(response);
            });
        },

        scrapeYoutube: function(tabs) {
            console.log('SCRAPING !');
            var vm = this;
            vm.showKeywords = false;
            vm.showSearchResults = false;
            if (!vm.youtubeLink) {
                return;
            }
            vm.showKeywordsLoading = true;
            this.$http.post('/scrape', { youtube: true, link: vm.youtubeLink }).then(response => {
                console.log('scrape ok');
                console.log(response);
                keywords = response.body.keywords;
                vm.keywords = []
                for (let kw of keywords) {
                    item = { value: kw, checked: true};
                    vm.keywords.push(item)
                }
                vm.showKeywordsLoading = false;
                vm.showKeywords = true;
            }, response => {
                vm.showKeywordsLoading = false;
                console.log('fffffffffff');
                console.log(response);
            });
        },

        scrapeAbstract: function(abstract, recursionLevel) {
            console.log('SCRAPING !');
            var vm = this;
            // vm.showKeywords = false;
            // vm.showSearchResults = false;
            this.$http.post('/scrape', { content: abstract }).then(response => {
                console.log('scrape ok');
                console.log(response);
                keywords = response.body.keywords;
                vm.keywords = []
                for (let kw of keywords) {
                    item = { value: kw, checked: true};
                    vm.keywords.push(item)
                }
                console.log(window.location.host);
                console.log(window.location.hostname);
                window.location.href = 'http://localhost:8000/?keywords=' + keywords.join(',') + '&recursion=' + (recursionLevel + 1);
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
            vm.showSearchResults = false;
            vm.showSearchLoading = true;
            keywords = []

            for (let kw in vm.keywords) {
                console.log(kw);
                if (vm.keywords[kw].checked) {
                    keywords.push(vm.keywords[kw].value)
                }
            }
            this.$http.post('/search', { content: keywords }).then(response => {
                console.log('search ok');
                console.log(response);
                vm.searchResults = response.body.results;
                vm.showSearchLoading = false;
                vm.showSearchResults = true;
            }, response => {
                vm.showSearchLoading = false;
                console.log('fffffffffff');
                console.log(response);
            });
        },

        uploadFile: function(tabs) {
            var vm = this;
            vm.showKeywords = false;
            vm.showKeywordsLoading = true;

            const files = document.querySelector('[type=file]').files;
            const formData = new FormData();

            for (let i = 0; i < files.length; i++) {
                let file = files[i];

                formData.append('files[]', file);
            }

            this.$http.post('/upload', formData).then(response => {
                console.log('upload ok');
                console.log(response);
                keywords = response.body.keywords;
                vm.keywords = []
                for (let kw of keywords) {
                    item = { value: kw, checked: true};
                    vm.keywords.push(item)
                }
                vm.showKeywordsLoading = false;
                vm.showKeywords = true;
            }, response => {
                vm.showKeywordsLoading = false;
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
                else if (e.target.classList.contains("upload-file")) {
                    this.uploadFile();
                }
                else if (e.target.classList.contains("scrape-youtube")) {
                    this.scrapeYoutube();
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
        var urlParams = new URLSearchParams(window.location.search);
        console.log(urlParams);
        var keywords = urlParams.get('keywords');
        var recursionLevel = urlParams.get('recursion');
        console.log(keywords);
        if (keywords) {
            keywords = keywords.split(',');
            this.keywords = []
            for (let kw of keywords) {
                item = { value: kw, checked: true};
                this.keywords.push(item)
            }
            this.showKeywords = true;
            this.searchDatasets();
        }
        if (recursionLevel) {
            this.recursionLevel = parseInt(recursionLevel);
        }
    }
})
