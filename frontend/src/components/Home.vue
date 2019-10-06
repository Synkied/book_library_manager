<template>
  <div class="app">
    <v-layout>
      <v-flex px-5 py-2>
        <v-card>
          <v-list two-line subheader>
            <v-subheader inset>Books</v-subheader>

            <v-list-item
              v-for="book in books"
              :key="book.title"
              @click="">
              <v-list-item-avatar>
                <v-icon
                  :class="[book.iconClass]"
                  v-text="book.icon"
                ></v-icon>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title v-text="book.title"></v-list-item-title>
                <v-list-item-subtitle v-text="book.author_name"></v-list-item-subtitle>
              </v-list-item-content>

              <v-list-item-action>
                <v-btn icon>
                  <v-icon color="grey lighten-1">edit</v-icon>
                </v-btn>
              </v-list-item-action>
              <v-list-item-action>
                <v-btn icon>
                  <v-icon color="grey lighten-1">delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>

            <v-divider inset></v-divider>

            <v-subheader inset>Authors</v-subheader>

            <v-list-item
              v-for="author in authors"
              :key="author.title"
              @click="">
              <v-list-item-avatar>
                <v-icon
                  :class="[author.iconClass]"
                  v-text="author.icon"
                ></v-icon>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title v-text="author.name"></v-list-item-title>
              </v-list-item-content>

              <v-list-item-action>
                <v-btn icon>
                  <v-icon color="grey lighten-1">edit</v-icon>
                </v-btn>
              </v-list-item-action>
              <v-list-item-action>
                <v-btn icon>
                  <v-icon color="grey lighten-1">delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card>

        <v-text-field
          v-model="bookInfos.title"
          label="Book title"/>
        <v-select
          :items="authors"
          v-model="bookInfos.author"
          label="Author"
          return-object
          item-text="name">
            <template v-slot:append-outer>
              <v-btn icon @click="addAuthorOverlay = !addAuthorOverlay">
                <v-icon small>add</v-icon>
              </v-btn>
            </template>
        </v-select>
        <v-overlay
          :absolute="true"
          :value="addAuthorOverlay">
          <v-text-field
            v-model="newBookAuthor"
            label="Book author"/>
          <v-btn
            @click="addAuthor();addAuthorOverlay = false">
            Add author
          </v-btn>
        </v-overlay>
        <v-btn @click="addBook()">Add book</v-btn>
      </v-flex>
      <v-btn color="success" @click="registerUser()">text</v-btn>
    </v-layout>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      bookInfos: {
        title: '',
        author: ''
      },
      newBookAuthor: '',
      authors: [],
      books: [],
      addAuthorOverlay: false
    }
  },
  methods: {
    async addBook (data) {
      let response
      if (data) {
        response = await this.$BackendAPI.bookPost(data)
      } else {
        data = {
          'author': this.bookInfos.author.id,
          'title': this.bookInfos.title
        }
        response = await this.$BackendAPI.bookPost(data)
      }
      console.log(response)
    },
    async addAuthor (data) {
      let response = await this.$BackendAPI.authorPost(data)
    },
    async getAuthors () {
      let response = await this.$BackendAPI.authorsGet()
      this.authors = response.data.authors
    },
    async getBooks () {
      let response = await this.$BackendAPI.booksGet()
      this.books = response.data.books
    },
    async registerUser (data) {
      let response
      if (data) {

      } else {
        data = {
          username: 'toto',
          email: 'toto@tutu.fr',
          password: 'tata'
        }
        response = await this.$BackendAPI.userRegister(data)
        console.log(response)
      }
    }
  },
  mounted () {
    this.getAuthors()
    this.getBooks()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
