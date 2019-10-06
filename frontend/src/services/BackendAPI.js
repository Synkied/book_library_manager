import axios from 'axios'

const BackendAPI = {
    install (Vue) {
        Vue.prototype.$BackendAPI = {
            async userRegister (data) {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}register`
                    console.log(data)
                    let response = await axios.post(url, data)
                    return response
                } catch (err) {
                    throw err.response
                }
            },
            async authorsGet () {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}api/authors`
                    let response = await axios.get(url)
                    return response
                } catch (err) {
                    throw err.response
                }
            },
            async authorPost (data) {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}api/authors`
                    let response = await axios.post(url, data)
                    return response
                } catch (err) {
                    throw err.response
                }
            },
            async booksGet () {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}api/books`
                    let response = await axios.get(url)
                    return response
                } catch (err) {
                    throw err.response
                }
            },
            async bookPost (data) {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}api/books`
                    let response = await axios.post(url, data)
                    return response
                } catch (err) {
                    throw err.response
                }
            },
        }
    }
}

export default BackendAPI
