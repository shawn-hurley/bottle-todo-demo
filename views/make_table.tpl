%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>The open items are as follows:</p>
<table border="1">
%for id, task in rows:
  <tr>
    <td><a href="/edit/{{id}}">{{id}}</a></td>
    <td>{{task}}</td>
  </tr>
%end
</table>
