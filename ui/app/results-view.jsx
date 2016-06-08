import React from 'react';
import ResultsTable from './results-table';
import ResultsMetadata from './results-metadata';

var ResultsView = React.createClass({

    getInitialState: function() {
        return {
            results: [],
            metadata: {},
        }
    },

    projectId: function() {
        return this.props.params.project_id || this.props.project_id;
    },

    buildId: function() {
        return this.props.params.build_id || this.props.build_id;
    },

    componentDidMount: function() {
        var url = "/api/" + this.projectId() + "/builds/" + this.buildId() +
                  "/results";
        this.buildsRequest = $.get(url, function(result) {
            this.setState({
                results: result.results,
                metadata: result.metadata,
            })
        }.bind(this))
    },

    componentWillUnmount: function() {
        this.buildsRequest.abort();
    },

    render: function() {
        return (
            <div>
                <h2 className="rs-page-title">Results</h2>
                <h3>Summary</h3>
                <ResultsMetadata metadata={this.state.metadata} />
                <h3>All results</h3>
                <ResultsTable results={this.state.results} />
            </div>
        );
    },

});

export default ResultsView;
