import React from 'react';
import ResultsTable from './results-table';

var LastFailedView = React.createClass({

    /**
     * This will populate all failed tests and how many times each failed 
     * in the last <count> executions for a specific build.
     */
    getInitialState: function() {
        return {
            results: []
        }
    },

    projectId: function() {
        return this.props.params.project_id || this.props.project_id;
    },

    buildName: function() {
        const result = this.props.params.build_name || this.props.build_name;
        return encodeURIComponent(result);
    },

    count: function() {
        return this.props.params.count || this.props.count;
    },

    componentDidMount: function() {
        var url = "/api/projects/" + this.projectId() + "/status/failed/count/" + 
                this.count() + "?build_name=" + this.buildName();
        this.lastFailedResultsRequest = $.get(url, function(result) {
            this.setState({
                results: result
            })
        }.bind(this))
    },

    componentWillUnmount: function() {
        this.lastFailedResultsRequest.abort();
    },

    render: function() {
        return (
            <div className="rs-embedded-list-table-wrapper rs-embedded-medium">
                <h2 className="rs-page-title">Last Failed</h2>
                <h3>Failed results</h3>
                <ResultsTable results={this.state.results} />
            </div>
        );
    },

});

export default LastFailedView;
