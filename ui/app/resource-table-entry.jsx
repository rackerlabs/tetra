import React from 'react';
import { Link } from 'react-router';

var ResourceTableEntry = React.createClass({

    render: function() {
        var resource = this.props.resource;
        var columnKeys = this.props.columnKeys;
        var columnLinks = this.props.columnLinks;
        return (
            <tr>
                { this.status(resource) }
                { this.columns(resource, columnKeys, columnLinks) }
            </tr>
        );
    },

    // todo: we need to be able to configure the column order
    columns: function(resource, columnKeys, columnLinks) {
        var result = [];
        for (var i = 0; i < columnKeys.length; i++) {
            var key = columnKeys[i];
            var val = resource[key];
            if (columnLinks[key]) {
                var link = columnLinks[key](resource);
                // check if value exists.  This is useful for when you just want to 
                // show actions
                if(val !== undefined) {
                    result.push(
                        <td key={i} className="rs-table-link">
                            <Link to={link}> {val} </Link>
                        </td>
                    );
                } else {
                    result.push(
                        <td key={i} className="rs-table-link">
                            <Link to={link}>
                                <button className="rs-btn rs-btn-primary">Go</button>
                            </Link>
                        </td>
                    );
                }
            } else {
                result.push(
                    <td key={i} className="rs-table-link"> {val} </td>
                );
            }
        }
        return result;
    },

    status:  function(resource) {
        var status = resource["result"] || resource["status"];
        if (status == "failed" || status == "error") {
            return <td className="rs-table-status rs-table-status-error"> </td>;
        } else if (status == "skipped"){
            return <td className="rs-table-status rs-table-status-warning"> </td>;
        }
        return <td className="rs-table-status rs-table-status-ok"> </td>;
    },

});

export default ResourceTableEntry;
