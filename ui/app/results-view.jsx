import React from 'react';
import ResultsTable from './results-table';
import ResultsMetadata from './results-metadata';

var ResultsView = React.createClass({

    getInitialState: function() {
        return {
            results: [],
            metadata: {},
            offset: 0
        }
    },

    projectId: function() {
        return this.props.params.project_id || this.props.project_id;
    },

    buildId: function() {
        return this.props.params.build_id || this.props.build_id;
    },

    componentDidMount: function() {
        this.getResults(this.state.offset)
    },

    componentWillUnmount: function() {
        this.buildsRequest.abort();
    },

    getResults: function(offset) {
        var url = "/api/projects/" + this.projectId() + "/builds/" + this.buildId() +
                  "/results?offset=" + offset;
        $.get(url, function(result) {
            this.setState({
                results: result.results,
                metadata: result.metadata,
                offset: offset,
            })
        }.bind(this))
    },

    offsetIncrease: function(event) {
        if(this.state.offset + 25 < this.state.metadata["total_results"]){
            this.getResults(this.state.offset + 25);
        }
        console.log(this.state.offset)
    },

    offsetDecrease: function(event) {
        if(this.state.offset - 25 <= 0){
            this.getResults(0);
        } else {
            this.getResults(this.state.offset - 25);
        }
        console.log(this.state.offset)
    },

    render: function() {
        var buttonStyle = {
            borderWidth: "1px",
            borderStyle: "solid",
            borderColor: "rgb(221, 221, 221)",
            borderRadius: "7px",
            paddingBottom: "5px",
            paddingTop: "5px",
            paddingLeft: "14px",
            paddingRight: "14px",
            fontSize: "14px",
            boxSizing: "border-box",
            textDecoration: "none"
        }
        var rowStyle = {
            marginBottom: "12px",
        }
        return (
            <div>
                <h2 className="rs-page-title">Results</h2>
                <h3>Summary</h3>
                <ResultsMetadata metadata={this.state.metadata} />
                <h3>All results</h3>
                <div className="rs-row" style={rowStyle} >
                  <div className="span-1" ><a style={buttonStyle}  href='#' onClick={this.offsetDecrease}>Previous</a></div>
                  <div className="span-1"><a style={buttonStyle}  href='#' onClick={this.offsetIncrease}>Next</a></div>
                  <div className="span-10"></div>
                </div>

                <ResultsTable results={this.state.results} />
            </div>
        );
    },

});

export default ResultsView;
