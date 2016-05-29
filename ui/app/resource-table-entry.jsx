import React from 'react';
import { Link } from 'react-router';

var ResourceTableEntry = React.createClass({

    render: function() {
        var resource = this.props.resource;
        var columnKeys = this.props.columnKeys.map(function(name) {
            return name.toLowerCase();
        });
        return (
            <tr>
                <td className="rs-table-status rs-table-status-ok"> </td>
                { this.columns(resource, columnKeys) }
            </tr>
        );
    },

    // todo: we need to be able to configure the column order
    columns: function(resource, columnKeys) {
        var result = [];
        for (var i = 0; i < columnKeys.length; i++) {
            var val = resource[columnKeys[i]];
            result.push(
                <td key={i} className="rs-table-link">
                    <Link to={this.props.link}> {val} </Link>
                </td>
            );
        }
        return result;
    },

});

export default ResourceTableEntry;
