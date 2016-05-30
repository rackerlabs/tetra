import React from 'react';
import ResourceTableEntry from './resource-table-entry';

var ResourceTable = React.createClass({

    render: function() {
        var headers = this.tableHeaders(this.props.columnTitles);
        var entries = this.tableEntries(this.props.resources,
                                        this.props.columnKeys);
        return (
            <table className="rs-list-table">
                {headers}
                {entries}
            </table>
        );
    },

    tableHeaders: function(headerNames) {
        return (
            <thead>
                <tr>
                    <th className="rs-table-status"></th>
                    { headerNames.map(this.tableHeader) }
                </tr>
            </thead>
        );
    },

    /* TODO: "At this time Canon does not provide javascript for handling sorting" */
    tableHeader: function(headerName, i) {
        return (
            <th key={i}>
                <a href ="#list-table" className="rs-table-sort">
                    <span className="rs-table-sort-text">{headerName}</span>
                    <span className="rs-table-sort-indicator"></span>
                </a>
            </th>
        );
    },

    tableEntries: function(resources, columnKeys) {
        var columnLinks = this.props.columnLinks;
        var entries = resources.map(function(resource, i) {
            return <ResourceTableEntry key={i}
                                       resource={resource}
                                       columnKeys={columnKeys}
                                       columnLinks={columnLinks} />
        });
        return (<tbody>{entries}</tbody>);
    },

});

export default ResourceTable;
