import React from 'react'
import axios from 'axios'
import loader from './giphy.gif' 

class Main extends React.Component {
    constructor() {
        super();
        this.handleSubmit = this.handleSubmit.bind(this);
        this.state = {
            loading: false,
            output: ""
        }
    }
    
    handleSubmit(event) {
        event.preventDefault();
        const data = new FormData(event.target);
        let news = "", title = "", author = ""
        for (let [key, value] of data.entries()) {
            if(key==="news")news=value
            if(key==="title")title=value
            if(key==="author")author=value
        }
        this.setState({
            loading: true
        }, () => {
            axios.get(`http://localhost:8000/fake_news/check?news=${news}&title=${title}&author=${author    }`)
            .then(res => {
                this.setState({
                    loading: false,
                    output: res.data.isTrue?"Real": "Fake"
                })
            })
            .catch(err => {
                this.setState({
                    loading: false
                })
                console.log(err)
            })    
        })
    }
    render(){
        return (
            <div className="row justify-content-center" style={{"padding": "10%", "alignContent": "center"}}>
                <div class="card col-sm-4" style={{"paddingTop": "5vh", "paddingBottom": "5vh"}}>
                    <form onSubmit={this.handleSubmit}>
                    <label htmlFor="news" style={{"fontSize": "20px", "marginBottom": "0vh"}}>Enter News</label>
                    <input
                        type="text"
                        className="form-control"
                        id="news"
                        name="news"
                        style={{"width": "50%", "margin":"auto"}}
                    />
                    <label htmlFor="title" style={{"fontSize": "20px" , "marginBottom": "0vh"}}>Enter Title</label>
                    <input
                        type="text"
                        className="form-control"
                        id="title"
                        name="title"
                        style={{"width": "50%", "margin":"auto"}}
                    />
                    <label htmlFor="author" style={{"fontSize": "20px" , "marginBottom": "0vh"}}>Enter Author</label>
                    <input
                        type="text"
                        className="form-control"
                        id="author"
                        name="author"
                        style={{"width": "50%", "margin":"auto"}}
                    />
                    <button className="btn btn-outline-primary" data-mdb-ripple-color="dark" style={{"margin-top": "1vh"}}>Submit!</button>
                    </form>
                    {this.state.loading ? <div style={{"height":"80px", "display":"flex", "alignItems":"center", "justifyContent":"center", "overflow":"hidden"}}><img src = {loader} alt = "Loading"/> </div>: <div>{this.state.output}</div>}
                </div>
            </div>
        )
    }
}

export default Main
