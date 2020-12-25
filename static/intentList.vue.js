const IntentList = {
  template: `
      <div>
        <h1>Content</h1>
          
          
      </div>`,
  data() {
    return {};
  },
  computed: {},
  mounted() {
    this.fetchPosts();
  },

  methods: {
    async fetchPosts() {
      if (!this.authstatus)
        // authstatus check here is not quite required, but is just a fall-back
        this.validationErrors.push(
          "Not logged in. You have to login to fetch posts."
        );
      else {
        console.log("Fetching posts..");
        // keywords passed as query - as-is.
        // verify whether server requires any specific format
        const res = await axios.get(
          `${this.urls.postget}?query=${this.keywords}&page=${
            this.currentPage + 1
          }`,
          {
            crossdomain: true,
          }
        );

        const postData = res.data;
        console.log(`GET posts done!`, postData);

        if (!postData["auth-status"]) {
          // auth-status is returned by post requests too!
          console.log("Auth denied..! Re-login.");
          this.validationErrors.push("Access is denied.");
        }

        this.posts = postData["posts"] ? postData["posts"] : [];
        this.currentPage = postData["currentpage"]
          ? postData["currentpage"]
          : 0;
        this.totalPages = postData["totalpages"] ? postData["totalpages"] : 0;

        // pagination logic yet to be implemented to navigate to subsequent pages
        console.log(".. posts fetched!");
      }
    },
  },

  validateAndSubmit() {
    //  there are no validations at this time.

    this.validationErrors = [];

    this.fetchPosts();
  },
};
