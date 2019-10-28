<template>
  <div class="app">
    <v-layout wrap justify-center>
      <v-flex xs5 px-5 py-2>
        <v-card>
          <v-card-title primary-title>
            Add a book
          </v-card-title>
          <v-card-text>
            <!-- Add a book instance -->
            <v-select
              :items="bookDescriptors"
              v-model="bookInfos.bookDescriptor"
              label="Book descriptor"
              item-value="id">
                <template v-slot:append-outer>
                  <v-btn icon @click="addBookDescriptorOverlay = !addBookDescriptorOverlay">
                    <v-icon small>add</v-icon>
                  </v-btn>
                </template>
                <template slot="selection" slot-scope="data">
                  <!-- HTML that describe how select should render selected items -->
                  {{ data.item.title }}, {{ data.item.author_name }}
                </template>
                <template slot="item" slot-scope="data">
                  <!-- HTML that describe how select should render items when the select is open -->
                  {{ data.item.title }}, {{ data.item.author_name }}
                </template>
            </v-select>
            <v-overlay
              :absolute="true"
              :value="addBookDescriptorOverlay">
              <v-text-field
                v-model="bookDescriptorInfos.title"
                label="Book title"/>
              <v-select
                :items="authors"
                v-model="bookDescriptorInfos.author"
                label="Author"
                return-object
                item-text="name">
                  <template v-slot:append-outer>
                    <v-btn icon @click="addAuthorOverlay = !addAuthorOverlay">
                      <v-icon small>add</v-icon>
                    </v-btn>
                  </template>
              </v-select>
              <v-btn
                @click="addBookDescriptor();addBookDescriptorOverlay = !addBookDescriptorOverlay">
                Add book descriptor
              </v-btn>
            </v-overlay>
            <v-text-field
              v-model="bookInfos.libraryLocation"
              label="Location"/>
            <v-btn @click="addBook()">Add book instance</v-btn>
          </v-card-text>
        </v-card>
      </v-flex>
      <v-spacer></v-spacer>
      <v-flex xs5 px-5 py-2>
        <v-card>
          <v-card-title primary-title>
            Add a book descriptor
          </v-card-title>
          <v-card-text>
            <!-- Add a book descriptor -->
            <v-text-field
              v-model="bookDescriptorInfos.title"
              label="Book title"/>
            <v-select
              :items="authors"
              v-model="bookDescriptorInfos.author"
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
            <v-btn @click="addBookDescriptor()">Add book descriptor</v-btn>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex px-5 py-2>
        <v-card>
          <v-list two-line subheader>
            <v-subheader inset>Books</v-subheader>
            <v-list-item
              v-for="book in books"
              :key="book.id"
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
                <v-btn @click="confirmModalBuilder('Book', book.title);bookToDelete = book" icon>
                  <v-icon color="grey lighten-1">delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card>
      </v-flex>
      <v-flex px-5 py-2>
        <v-card>
          <v-list two-line subheader>
            <v-subheader inset>Book Descriptors</v-subheader>

            <v-list-item
              v-for="bookDescriptor in bookDescriptors"
              :key="bookDescriptor.title"
              @click="">
              <v-list-item-avatar>
                <v-icon
                  :class="[bookDescriptor.iconClass]"
                  v-text="bookDescriptor.icon"
                ></v-icon>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title v-text="bookDescriptor.title"></v-list-item-title>
                <v-list-item-subtitle v-text="bookDescriptor.author_name"></v-list-item-subtitle>
              </v-list-item-content>


              <v-list-item-action>
                <v-btn @click="confirmModalBuilder('BookDescriptor', bookDescriptor.title);bookDescriptorToDelete = bookDescriptor" icon>
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
                <v-btn @click="confirmModalBuilder('Author', author.name);authorToDelete = author.name" icon>
                  <v-icon color="grey lighten-1">delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card>
        <v-btn color="primary" @click="registerUser()">Add fake user</v-btn>
        <v-btn color="grey" @click="deleteUser()">Remove fake user</v-btn>
      </v-flex>
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
    v-if="confirmDeleteBookDescriptor.display"
    :toolbarMsg='confirmDeleteBookDescriptor.toolbarMsg'
    :bodyMsg='confirmDeleteBookDescriptor.bodyMsg'
    :okBtnText='confirmDeleteBookDescriptor.okBtnText'
    :cancelBtnText='confirmDeleteBookDescriptor.cancelBtnText'
    :autofocus='confirmDeleteBookDescriptor.autofocus'
    @action="deleteBookDescriptor(bookDescriptorToDelete)"
    @close="confirmDeleteBookDescriptor.display = false">
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
      bookDescriptorInfos: {
        title: '',
        author: ''
      },
      bookInfos: {
        bookDescriptor: '',
        libraryLocation: ''
      },
      newBookAuthor: '',
      newBookDescriptor: {
        title: '',
        author: ''
      },
      authors: [],
      bookDescriptors: [],
      books: [],
      addAuthorOverlay: false,
      addBookDescriptorOverlay: false,
      authorToDelete: '',
      bookDescriptorToDelete: '',
      bookToDelete: '',
      confirmDeleteAuthor: {
        display: false,
        toolbarMsg: '',
        bodyMsg: '',
        okBtnText: '',
        cancelBtnText: '',
        autofocus: ''
      },
      confirmDeleteBookDescriptor: {
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
    async getBookDescriptors () {
      try {
        let response = await this.$BackendAPI.bookDescriptorsGet()
        this.bookDescriptors = response.data.book_descriptors
      } catch (err) {
        console.error(err.response)
      }
    },
    async addBookDescriptor (data) {
      try {
        let response
        if (data) {
          response = await this.$BackendAPI.bookDescriptorPost(data)
        } else {
          data = {
            'author': this.bookDescriptorInfos.author.id,
            'title': this.bookDescriptorInfos.title
          }
          response = await this.$BackendAPI.bookDescriptorPost(data)
        }
        this.getBookDescriptors()
        this.bookDescriptorInfos.author = ''
        this.bookDescriptorInfos.title = ''
      } catch (err) {
        console.error(err)
      }
    },
    async deleteBookDescriptor (book) {
      try {
        let bookDescriptorToDelete = {}
        bookDescriptorToDelete.title = book.title
        bookDescriptorToDelete.author = book.author
        console.log(bookDescriptorToDelete)
        let response = await this.$BackendAPI.bookDescriptorDelete(bookDescriptorToDelete)
        this.getBookDescriptors()
      } catch (err) {
        console.error(err.response)
      }
    },
    async deleteBook (book) {
      try {
        let bookToDelete = {}
        bookToDelete.title = book.title
        bookToDelete.author = book.author
        console.log(bookToDelete)
        let response = await this.$BackendAPI.bookDelete(bookToDelete)
        this.getBookDescriptors()
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
        this.getBookDescriptors()
      } catch (err) {
        console.error(err.response)
      }
    },
    async getBooks () {
      try {
        let response = await this.$BackendAPI.booksGet()
        this.books = response.data.books.map(book => {
            let matchingBookDescriptor = this.bookDescriptors.filter(bookDescriptor => bookDescriptor.id === book.book_descriptor)[0]
            book.title = matchingBookDescriptor.title
            book.author_name = matchingBookDescriptor.author_name
            return book
        })
      } catch (err) {
        console.error(err)
      }
    },
    async addBook (data) {
      try {
        let response
        if (data) {
          response = await this.$BackendAPI.bookPost(data)
        } else {
          data = {
            'book_descriptor': this.bookInfos.bookDescriptor,
            'library_location': this.bookInfos.libraryLocation
          }
          response = await this.$BackendAPI.bookPost(data)
        }
        this.getBookDescriptors()
        this.getBooks()
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
      if (type === 'BookDescriptor') {
        this.confirmDeleteBookDescriptor.display = true
        this.confirmDeleteBookDescriptor.toolbarMsg = `Delete ${type}: ${name}`
        this.confirmDeleteBookDescriptor.bodyMsg = `Do you really want to delete ${type}: ${name}?`
        this.confirmDeleteBookDescriptor.okBtnText = 'Yes'
        this.confirmDeleteBookDescriptor.cancelBtnText = 'No'
        this.confirmDeleteBookDescriptor.autofocus = 'No'
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
  async mounted () {
    await this.getAuthors()
    await this.getBookDescriptors()
    await this.getBooks()
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
