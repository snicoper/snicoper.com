/*globals Cookies delimiters, toastr*/

function ArticleRatioVoteVue () {
  new Vue({
    el: '#article-ratio-vote-vue',
    delimiters: delimiters,
    data: {
      article_id: 0,
      positives: 0,

      positive_cookie_name: '',

      cam_vote_positive: true,

      urls: {
        details: '',
        positive: '',
      }
    },

    mounted () {
      const data = $('#article-data');
      this.article_id = data.data('article-id');
      this.urls.positive = data.data('url-article-vote-positive');
      this.urls.details = data.data('url-article-vote-details');
      this.positive_cookie_name = `vote_positive_article_${this.article_id}`;

      if (Cookies.get(this.positive_cookie_name)) {
        this.cam_vote_positive = false;
      }

      this._getVoteDetails();
    },

    methods: {
      onVotePositive () {
        axios.put(this.urls.positive, {
          'article': this.article_id,
        }).then((response) => {
          if (response.status === 200) {
            Cookies.set(this.positive_cookie_name, 1);
            this.cam_vote_positive = false;
            this._getVoteDetails();
            toastr.success('Gracias el positivo!');
          }
        }).catch(() => {
          toastr.error('Ha ocurrido un error, intentalo mas tarde');
        });
      },

      _getVoteDetails () {
        axios.get(this.urls.details)
          .then((response) => {
            if (response.status === 200) {
              this.positives = response.data.positives;
            }
          });
      },
    }
  });
}
