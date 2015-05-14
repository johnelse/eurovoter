% rebase('base.tpl', jquery=False, logout_link=logout_link)
        <h4>{{message}}</h4>
% if start_link:
        <p><a href="/">Start</a></p>
% end
