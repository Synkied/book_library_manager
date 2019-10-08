import axios from 'axios'

const BackendAPI = {
    install (Vue) {
        Vue.prototype.$BackendAPI = {
            async userRegister (data) {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}user/register`
                    let response = await axios.post(url, data)
                    return response
                } catch (err) {
                    throw err
                }
            },
            async userDelete (data) {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}user/delete`
                    let response = await axios.post(url, data)
                    return response
                } catch (err) {
                    throw err
                }
            },
            async authorsGet () {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}api/author`
                    let response = await axios.get(url)
                    return response
                } catch (err) {
                    throw err
                }
            },
            async authorPost (data) {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}api/author`
                    let response = await axios.post(url, data)
                    return response
                } catch (err) {
                    throw err
                }
            },
            async authorDelete (data) {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}api/author/delete`
                    let response = await axios.post(url, data)
                    return response
                } catch (err) {
                    throw err
                }
            },
            async booksGet () {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}api/book`
                    let response = await axios.get(url)
                    return response
                } catch (err) {
                    throw err
                }
            },
            async bookPost (data) {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}api/book`
                    let response = await axios.post(url, data)
                    return response
                } catch (err) {
                    throw err
                }
            },
            async bookDelete (data) {
                try {
                    let url = `${process.env.VUE_APP_backendAPIURL}api/book/delete`
                    let response = await axios.post(url, data)
                    return response
                } catch (err) {
                    throw err
                }
            },
        }
    }
}

export default BackendAPI
