import React, { Component } from "react";
import axios from "axios";

export class GetDjango extends Component {
  constructor(props) {
    super(props);

    this.state = {
      articleData: [],
      changed: false,
      loading: false,
      title: "",
      email: "",
      author: "",
      editing: false,
      editingId: 0,
    };
    this.fetchData = this.fetchData.bind(this);
    this.onChange = this.onChange.bind(this);
    this.onSave = this.onSave.bind(this);
  }
  componentDidMount() {
    this.fetchData();
  }
  fetchData() {
    this.setState({
      loading: true,
    });
    axios
      .get("http://127.0.0.1:8000/api/articles/")
      .then((res) => {
        this.setState({
          ...this.state,
          articleData: res.data,
          loading: false,
        });
      })
      .catch((error) => console.error(error));
  }
  deleteArticle(id) {
    let newList = this.state.articleData.filter((article) => article.id !== id);
    this.setState({
      ...this.state,
      articleData: newList,
      changed: true,
    });
    return axios
      .delete(`http://127.0.0.1:8000/api/articles/${id}/`)
      .then((res) => console.log(res.data))
      .catch((err) => console.error(err));
  }
  onChange({ target }) {
    this.setState({
      ...this.state,
      [target.name]: target.value,
    });
  }
  onSave() {
    if (this.state.editing) {
      axios
        .post("http://127.0.0.1:8000/api/articles/", {
          title: this.state.title,
          author: this.state.author,
          email: this.state.email,
        })
        .then((res) => {
          this.setState({
            ...this.state,
            changed: true,
            title: "",
            email: "",
            author: "",
          });
          console.log(res.data);
          this.fetchData();
        })
        .catch((err) => console.error(err));
    } else {
      axios
        .put(`http://127.0.0.1:8000/api/articles/${this.state.editingId}/`, {
          title: this.state.title,
          author: this.state.author,
          email: this.state.email,
        })
        .then((res) => {
          this.setState({
            ...this.state,
            title: "",
            email: "",
            author: "",
            editing: false,
          });
          console.log(res.data);
          this.fetchData();
        })
        .catch((err) => console.error(err));
    }
  }
  editArticle(article) {
      window.scrollTo(0,0);
    this.setState({
      title: article.title,
      email: article.email,
      author: article.author,
      editingId: article.id,
      editing: false,
    });
  }
  render() {
    var isLoading = this.state.loading;
    var articleData = this.state.articleData;
    return (
      <div>
        {isLoading ? (
          <h1>Loading...</h1>
        ) : (
          <div className="wrapper bg-light container pt-3 pl-3">
            {this.state.changed ? (
              <p className="ml-5 text-success">Your changes has been saved</p>
            ) : null}
            <h3>Articles</h3>
            <i>Add new article/ edit existing</i>
            <div className="form-group">
              <label htmlFor="new-article-title">Title:</label>
              <input
                type="text"
                onChange={(e) => this.onChange(e)}
                name="title"
                className="form-control"
                value={this.state.title}
              />
              <label htmlFor="new-article-title">Email: </label>
              <input
                type="email"
                onChange={(e) => this.onChange(e)}
                name="email"
                className="form-control"
                value={this.state.email}
              />
              <label htmlFor="new-article-title">Author: </label>
              <input
                type="text"
                onChange={(e) => this.onChange(e)}
                name="author"
                className="form-control"
                value={this.state.author}
              />
              <button onClick={this.onSave} className="btn btn-primary mt-3">
                Save
              </button>
            </div>
            {articleData.map((article) => (
              <div
                key={article.id}
                className="article-info card bg-light p-5 mt-3"
              >
                <h1>
                  {article.title} - {article.id}
                </h1>
                <p className="text-warning">{article.email}</p>
                <b>{article.author}</b>
                <button
                  className="btn btn-danger mt-3"
                  onClick={this.deleteArticle.bind(this, article.id)}
                >
                  Delete
                </button>
                <button
                  className="btn btn-warning mt-3"
                  onClick={this.editArticle.bind(this, article)}
                >
                  Edit
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }
}

export default GetDjango;
