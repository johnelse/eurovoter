% rebase('base.tpl', logout_link=False, scripts=[])
      <div class="u-full-width" style="margin-top: 5%">
        <h4>Results</h4>
      </div>
      <table class="u-full-width">
        <thead>
          <tr>
            <th>Country</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
% for country, score in results:
          <tr>
            <td>{{country}}</td>
            <td>{{score}}</td>
          <tr>
% end
        </tbody>
      </table>
