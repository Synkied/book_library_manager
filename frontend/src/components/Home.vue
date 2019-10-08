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
                <v-btn @click="confirmModalBuilder('Book', book.title);bookToDelete = book" icon>
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
                <v-btn @click="confirmModalBuilder('Author', author.name);authorToDelete = author.name" icon>
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
            @click="addAuthor();addAuthorOverlay = !addAuthorOverlay">
            Add author
          </v-btn>
        </v-overlay>
        <v-btn @click="addBook()">Add book</v-btn>
      </v-flex>
      <v-btn color="success" @click="registerUser()">text</v-btn>
      <v-btn color="error" @click="deleteUser()">text</v-btn>
    </v-layout>

  <confirmModal
    v-if="confirmDeleteAuthor.display"
    :toolbarMsg='confirmDeleteAuthor.toolbarMsg'
    :bodyMsg='confirmDeleteAuthor.bodyMsg'
    :okBtnText='confirmDeleteAuthor.okBtnText'
    :cancelBtnText='confirmDeleteAuthor.cancelBtnText'
    :autofocus='confirmDeleteAuthor.autofocus'
    @action="deleteAuthor(authorToDelete)"
    @close="confirmDeleteAuthor.display = false">
  </confirmModal>

  <confirmModal
    v-if="confirmDeleteBook.display"
    :toolbarMsg='confirmDeleteBook.toolbarMsg'
    :bodyMsg='confirmDeleteBook.bodyMsg'
    :okBtnText='confirmDeleteBook.okBtnText'
    :cancelBtnText='confirmDeleteBook.cancelBtnText'
    :autofocus='confirmDeleteBook.autofocus'
    @action="deleteBook(bookToDelete)"
    @close="confirmDeleteBook.display = false">
  </confirmModal>

  </div>
</template>

<script>
import confirmModal from './confirmModal'

export default {
  name: 'Home',
  components: {
    confirmModal
  },
  data() {
    return {
      bookInfos: {
        title: '',
        author: ''
      },
      newBookAuthor: '',
      authors: [],
      books: [],
      addAuthorOverlay: false,
      authorToDelete: '',
      bookToDelete: '',
      confirmDeleteAuthor: {
        display: false,
        toolbarMsg: '',
        bodyMsg: '',
        okBtnText: '',
        cancelBtnText: '',
        autofocus: ''
      },
      confirmDeleteBook: {
        display: false,
        toolbarMsg: '',
        bodyMsg: '',
        okBtnText: '',
        cancelBtnText: '',
        autofocus: ''
      }
    }
  },
  methods: {
    async addBook (data) {
      try {
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
      } catch (err) {
        console.error(err.response)
      }
    },
    async deleteBook (book) {
      try {
        let bookToDelete = {}
        bookToDelete.title = book.title
        bookToDelete.author = book.author
        let response = await this.$BackendAPI.bookDelete(bookToDelete)
        this.getBooks()
      } catch (err) {
        console.error(err.response)
      }
    },
    async addAuthor (data) {
      try {
        let response
        if (data) {
          response = await this.$BackendAPI.authorPost(data)
        } else {
          data = {
            'name': this.newBookAuthor
          }
          response = await this.$BackendAPI.authorPost(data)
        }
        this.getAuthors()
      } catch (err) {
        console.error(err.response)
      }
    },
    async deleteAuthor (name) {
      try {
        let authorToDelete = {}
        authorToDelete.name = name
        let response = await this.$BackendAPI.authorDelete(authorToDelete)
        this.getAuthors()
      } catch (err) {
        console.error(err.response)
      }
    },
    async getAuthors () {
      try {
        let response = await this.$BackendAPI.authorsGet()
        this.authors = response.data.authors
      } catch (err) {
        console.error(err.response)
      }
    },
    async getBooks () {
      try {
        let response = await this.$BackendAPI.booksGet()
        this.books = response.data.books
      } catch (err) {
        console.error(err.response)
      }
    },
    async registerUser (data) {
      try {
        let response
        if (data) {
          response = await this.$BackendAPI.userRegister(data)
        } else {
          data = {
            username: 'toto',
            email: 'toto@tutu.fr',
            password: 'tata'
          }
          response = await this.$BackendAPI.userRegister(data)
          }
      } catch (err) {
        console.error(err.response)
      }
    },
    async deleteUser (data) {
      try {
        let response
        if (data) {
          response = await this.$BackendAPI.userDelete(data)
        } else {
          data = {
            username: 'toto',
          }
          response = await this.$BackendAPI.userDelete(data)
          }
      } catch (err) {
        console.error(err.response)
      }
    },
    confirmModalBuilder (type, name, action) {
      if (type === 'Author') {
        this.confirmDeleteAuthor.display = true
        this.confirmDeleteAuthor.toolbarMsg = `Delete ${type}: ${name}`
        this.confirmDeleteAuthor.bodyMsg = `Do you really want to delete ${type}: ${name}?`
        this.confirmDeleteAuthor.okBtnText = 'Yes'
        this.confirmDeleteAuthor.cancelBtnText = 'No'
        this.confirmDeleteAuthor.autofocus = 'No'
      }
      if (type === 'Book') {
        this.confirmDeleteBook.display = true
        this.confirmDeleteBook.toolbarMsg = `Delete ${type}: ${name}`
        this.confirmDeleteBook.bodyMsg = `Do you really want to delete ${type}: ${name}?`
        this.confirmDeleteBook.okBtnText = 'Yes'
        this.confirmDeleteBook.cancelBtnText = 'No'
        this.confirmDeleteBook.autofocus = 'No'
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
