<template>
    <div id="popup-content">
        <div class="button scrape">Scrape</div>
        <div v-if="showKeywordsLoading" id="keywords-title" class="sub-title">Loading ...</div>
        <div id="keywords-title" class="sub-title hidden">Keywords:</div>
        <ul v-if="showKeywords">
            <li class="generic-list" v-for="kw in keywords">
                {{ kw }}
            </li>
        </ul>
        <div class="button search">Search</div>
        <div v-if="showSearchLoading" id="keywords-title" class="sub-title">Loading ...</div>
        <div id="datasets-title" class="sub-title hidden">Results:</div>
        <ul v-if="showSearchResults">
            <li v-for="res in searchResults.datasets">
                <div><strong>Title: </strong>{{ res.title }}</div>
                <div><strong>Abstract: </strong>{{ res.abstract.substr(0, 100) }}</div>
                <template v-for="link in res.links">
                    <div><strong>URL: </strong><a v-bind:href="link">{{ link }}</a></div>
                </template>
                <hr />
            </li>
        </ul>
        <div v-show="totalResponseCount" class="button show-more">Show more results</div>
        <div id="error-content" class="hidden">
            <p>Can't execute content script on this page. Check extension configuration.</p>
        </div>
    </div>
</template>

<script>
    // export default { }
    module.exports = {
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
                totalResponseCount: null,
                showKeywordsLoading: false,
                showSearchLoading: false,
            }
        },
        methods: {
            sendScrapeActionToTab: function(tabs) {
                var vm = this;
                vm.showKeywords = false;
                vm.showSearchResults = false;
                vm.showKeywordsLoading = true;
                browser.tabs.sendMessage(
                    tabs[0].id,
                    { action: 'scrape' }
                ).then(response => {
                    console.log("Message from the content script scrape:");
                    console.log(response);
                    vm.keywords = response.keywords;
                    vm.showKeywordsLoading = false;
                    vm.showKeywords = true;
                }).catch(function(err) {
                    vm.showKeywordsLoading = false;
                    console.log('ffffffffff');
                    console.log(err);
                });
            },

            searchDatasets: function(tabs) {
                // search request wouldn't normally require involvement from the tab content script,
                // but for some reason http requests do not work from the background script.......
                console.log('searching datasets...');
                var vm = this;
                vm.showSearchLoading = true;
                browser.tabs.sendMessage(
                    tabs[0].id,
                    { action: 'search', keywords: vm.keywords }
                ).then(response => {
                    console.log("Message from the content script search:");
                    console.log(response);
                    vm.totalResponseCount = response.results.datasets.length
                    vm.searchResults = response.results;
                    vm.showSearchLoading = false;
                    vm.showSearchResults = true;
                }).catch(function(err) {
                    vm.showSearchLoading = false;
                    console.log('fffffffff');
                    console.log(err);
                });
            },

            showMore: function(tabs) {
                var vm = this;
                var creating = browser.tabs.create({
                    url:"http://localhost:8000?keywords=" + vm.keywords.join(',')
                });
            },

            listenForClicks: function() {
                document.addEventListener("click", (e) => {
                    // console.log(e.target.classList);
                    if (e.target.classList.contains("scrape")) {
                        browser.tabs.query({ active: true, currentWindow: true })
                            .then(this.sendScrapeActionToTab)
                            .catch(error => {
                                console.error(err);
                            });
                    }
                    else if (e.target.classList.contains("search")) {
                        browser.tabs.query({ active: true, currentWindow: true })
                            .then(this.searchDatasets)
                            .catch(error => {
                                console.error(err);
                            });
                    }
                    else if (e.target.classList.contains("show-more")) {
                        browser.tabs.query({ active: true, currentWindow: true })
                            .then(this.showMore)
                            .catch(error => {
                                console.error(err);
                            });
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
            browser.tabs.executeScript({file: "/content_scripts/content_script.js"})
                .then(this.listenForClicks)
                .catch(this.reportExecuteScriptError);
        }
    }
</script>

<style scoped>
    .hidden {
        display: none;
    }
    .button {
        border: 1px solid black;
        padding: 3px;
        margin: 3% auto;
        padding: 4px;
        text-align: center;
        font-size: 1.5em;
        cursor: pointer;
    }
    .popup-content {
        height: 20em;
            width: 20em;
    }
    .generic-list {
        text-align: center;
    }
    .sub-title {
        text-align: center;
    }
    .show-more {

    }
</style>
