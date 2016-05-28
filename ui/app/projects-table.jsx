import React from 'react';

/* TODO: "At this time Canon does not provide javascript for handling sorting" */
var ProjectsTable = React.createClass({

    render: function() {
        return (
            <table className="rs-list-table">
                {this.tableHeaders()}
                {this.tableEntries()}
            </table>
        );
    },

    tableHeaders: function() {
        var headerNames = ["Id", "Name"];
        return (
            <thead>
                <tr>
                    <th className="rs-table-status"></th>
                    { headerNames.map(this.tableHeader) }
                </tr>
            </thead>
        );
    },

    tableHeader: function(headerName, i) {
        return (
            <th key={i}>
                <a href="#list-table" className="rs-table-sort">
                    <span className="rs-table-sort-text">{headerName}</span>
                    <span className="rs-table-sort-indicator"></span>
                </a>
            </th>
        );
    },

    tableEntries: function() {
        var entries = [];
        for (var i = 0; i < this.props.projects.length; i++) {
            entries.push(
                <tr key={i}>
                    <td className="rs-table-status rs-table-status-ok"></td>
                    <td>{this.props.projects[i].id}</td>
                    <td>{this.props.projects[i].name}</td>
                </tr>
            );

        }

        return (<tbody>{entries}</tbody>);
    },

});

export default ProjectsTable;
