% rebase('base.tpl',
%        logout_link=True,
%        scripts=['jquery-2.1.4.min.js', 'formsubmit.js'])
      <div class="u-full-width" style="margin-top: 5%">
        <h4>Welcome, {{name.title()}}!</h4>
        <p>Choose wisely:</p>
      </div>
      <form id="voting">
% for score in scores:
        <label for="{{score}}points">{{score}} points</label>
        <select class="u-full-width" name="{{score}}points">
          <option value="None">-- Choose --</option>
%   for country_id, name in countries:
          <option value="{{country_id}}">{{name}}</option>
%   end
        </select>
% end
        <input class="button-primary" value="submit" type="button" id="submit">
        <div class="u-full-width" id="results">---</div>
      </form>
