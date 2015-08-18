__all__ = ["LoginManagerWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from pyasm.search import Search
from alternative_elements.customcheckbox import * 

class LoginManagerWdg(BaseRefreshWdg):

    def init(my):
        nothing = 'true' 
        my.countries = ["United States","Afghanistan","Akrotiri","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla","Antarctica","Antigua and Barbuda","Argentina","Armenia","Aruba","Ashmore and Cartier Islands","Australia","Austria","Azerbaijan","Bahamas, The","Bahrain","Bangladesh","Barbados","Bassas da India","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Bouvet Island","Brazil","British Indian Ocean Territory","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burma","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China","Christmas Island","Clipperton Island","Cocos (Keeling) Islands","Colombia","Comoros","Congo, Democratic Republic of the","Congo, Republic of the","Cook Islands","Coral Sea Islands","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Dhekelia","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Europa Island","Falkland Islands (Islas Malvinas)","Faroe Islands","Fiji","Finland","France","French Guiana","French Polynesia","French Southern and Antarctic Lands","Gabon","Gambia, The","Gaza Strip","Georgia","Germany","Ghana","Gibraltar","Glorioso Islands","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guernsey","Guinea","Guinea-Bissau","Guyana","Haiti","Heard Island and McDonald Islands","Holy See (Vatican City)","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Jan Mayen","Japan","Jersey","Jordan","Juan de Nova Island","Kazakhstan","Kenya","Kiribati","Korea, North","Korea, South","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Martinique","Mauritania","Mauritius","Mayotte","Mexico","Micronesia, Federated States of","Moldova","Monaco","Mongolia","Montserrat","Morocco","Mozambique","Namibia","Nauru","Navassa Island","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","Norfolk Island","Northern Mariana Islands","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paracel Islands","Paraguay","Peru","Philippines","Pitcairn Islands","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Helena","Saint Kitts and Nevis","Saint Lucia","Saint Pierre and Miquelon","Saint Vincent and the Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia and Montenegro","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Georgia and the South Sandwich Islands","Spain","Spratly Islands","Sri Lanka","Sudan","Suriname","Svalbard","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor-Leste","Togo","Tokelau","Tonga","Trinidad and Tobago","Tromelin Island","Tunisia","Turkey","Turkmenistan","Turks and Caicos Islands","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Vanuatu","Venezuela","Vietnam","Virgin Islands","Wake Island","Wallis and Futuna","West Bank","Western Sahara","Yemen","Zambia","Zimbabwe"]
        my.states = ["Alabama","Alaska","American Samoa","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","District of Columbia","Florida","Georgia","Guam","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Northern Marianas Islands","Ohio","Oklahoma","Oregon","Pennsylvania","Puerto Rico","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Virgin Islands","Washington","West Virginia","Wisconsin","Wyoming"]


    def switch_person(my):
        behavior = {'css_class': 'change', 'type': 'change', 'cbjs_action': '''
                        try{
                           var top_el = spt.api.get_parent(bvr.src_el, '.login_manager_wdg');
                           person_code = bvr.src_el.value;
                           if(person_code != 'NEW'){
                               spt.api.load_panel(top_el, 'login_manager.LoginManagerWdg', {'person_code': person_code});
                           }else{
                               spt.api.load_panel(top_el, 'login_manager.LoginManagerWdg');
                           }
                           red_row = top_el.getElementById('red_row'); 
                           red_row.style.display = 'none';
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def add_company(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function replaceAll(find, replace, str) {
                          find = find.replace('[','\\\[').replace(']','\\\]').replace('+','\\\+');
                          return str.replace(new RegExp(find, 'g'), replace);
                        }
                        function getRandomInt(min, max) {
                            return Math.floor(Math.random() * (max - min + 1)) + min;
                        }
                        function reverse(s){
                            return s.split("").reverse().join("");
                        }
                        try{
                            new_name = prompt('What is the name of the Company?');
                            if(new_name != '' && new_name != null){
                                new_upper = new_name.toUpperCase();
                                server = TacticServerStub.get();
                                exists = server.eval("@SOBJECT(twog/company['name','" + new_upper + "'])");
                                if(exists.length == 0){
                                    new_company = server.insert('twog/company', {'name': new_upper});
                                    var top_el = spt.api.get_parent(bvr.src_el, '.login_manager_wdg');
                                    company_sel = top_el.getElementById('company_code');
                                    company_sel.innerHTML = company_sel.innerHTML + '<option value="' + new_company.code + '">' + new_company.name + "</option>";
                                    company_sel.value = new_company.code;
                                    if(confirm("Would you like '" + new_name + "' to also be designated a 'Client'?")){
                                        exists2 = server.eval("@SOBJECT(twog/client['name','" + new_name + "'])");
                                        if(exists2.length == 0){
                                            new_client = server.insert('twog/client', {'name': new_name, 'billing_status': 'No Billing Problems'});
                                            server.update(new_company.__search_key__, {'client_code': new_client.code});
                                            attempted_login = replaceAll(' ','',new_name.toLowerCase());
                                            if(attempted_login.length > 5){
                                                attempted_login = attempted_login.substr(0,5);
                                            }
                                            attempted_login = 'gg_' + attempted_login;
                                            login_inserted = false;
                                            while(!login_inserted){
                                                random_num = getRandomInt(100, 999);
                                                attempted_login = attempted_login + String(random_num);
                                                anyofem = server.eval("@SOBJECT(sthpw/login['login','" + attempted_login + "'])");
                                                if(anyofem.length == 0){
                                                    english_pass = reverse(attempted_login) + String(getRandomInt(100, 999)); 
                                                    passwo = spt.md5(english_pass); 
                                                    new_per = server.insert('twog/person', {'login_name': attempted_login, 'first_name': new_name, 'last_name': 'Portal Account', 'email': 'portal.account@2gdigital.com', 'client_code': new_client.code, 'company_code': new_company.code});
                                                    server.insert('sthpw/login', {'login': attempted_login, 'code': attempted_login, 'first_name': new_name, 'last_name': 'Portal Account', 'password': passwo, 'license_type': 'user', 'email': 'portal.account@2gdigital.com', 'display_name': 'Portal Account, ' + new_name, 'location': 'external'});
                                                    server.insert('sthpw/login_in_group', {'login_group': 'client', 'login': attempted_login});
                                                    server.update(new_client.__search_key__, {'portal_login': attempted_login, 'portal_pass': english_pass});
                                                    login_inserted = true;
                                                }
                                            }
                                            
                                        }else{
                                            alert("A Client with the name " + new_name + " already exists.");
                                        }
                                    }
                                }else{
                                    alert("A Company with name '" + new_name + "' already exists.");
                                } 
                            }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_save(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function oc(a){
                            var o = {};
                            for(var i=0;i<a.length;i++){
                                o[a[i]]='';
                            }
                            return o;
                        }
                        function replaceAll(find, replace, str) {
                          find = find.replace('[','\\\[').replace(']','\\\]').replace('+','\\\+');
                          return str.replace(new RegExp(find, 'g'), replace);
                        }
                        function getRandomInt(min, max) {
                            return Math.floor(Math.random() * (max - min + 1)) + min;
                        }
                        function reverse(s){
                            return s.split("").reverse().join("");
                        }
                        function create_login(insert_dict, person_obj, location, license_type){
                            server = TacticServerStub.get();
                            attempted_name = insert_dict['first_name'].split(' ')[0].toLowerCase() + '.' + insert_dict['last_name'].split(' ')[0].toLowerCase();
                            next_attempted_name = attempted_name;
                            inserted = false;
                            count = 0;
                            pass = '';
                            is_external = false;
                            if(location == 'external'){
                                is_external = true;
                            }
                            while(!inserted){
                                already_there = server.eval("@SOBJECT(sthpw/login['login','" + next_attempted_name + "'])");
                                if(already_there.length > 0){
                                    count = count + 1;
                                    next_attempted_name = attempted_name + String(count);
                                }else{
                                    pass = '2g' + insert_dict['last_name'].toLowerCase();
                                    new_login_name = next_attempted_name;
                                    attempted_name = new_login_name;
                                    md5_pass = spt.md5(pass);
                                    server.update(person_obj.__search_key__, {'login_name': attempted_name});
                                    //Now need to add them to default groups
                                    if(!is_external){
                                        company = server.eval("@SOBJECT(twog/company['name','2G DIGITAL POST'])")[0];
                                        server.update(person_obj.__search_key__, {'company_code': company.code, 'client_code': company.client_code});
                                    }
                                    server.insert('sthpw/login', {'login': attempted_name, 'code': attempted_name, 'first_name': insert_dict['first_name'], 'last_name': insert_dict['last_name'], 'password': md5_pass, 'email': insert_dict['email'], 'license_type': license_type, 'phone_number': insert_dict['main_phone'], 'location': location, 'display_name': insert_dict['last_name'] + ', ' + insert_dict['first_name']});
                                    if(is_external){
                                        server.insert('sthpw/login_in_group', {'login_group': 'client', 'login': attempted_name});
                                    }
                                    inserted = true;
                                }
                            }
                            return {'login': attempted_name, 'pass': pass};
                        }
 
                        try{
                            server = TacticServerStub.get();
                            var top_el = spt.api.get_parent(bvr.src_el, '.login_manager_wdg');
                            all_els = top_el.getElementsByClassName('spt_input'); 
                            insert_dict = {};
                            login_logic = {};
                            for(var r = 0; r < all_els.length; r++){
                                guys_id = all_els[r].id;
                                if(guys_id != 'person_selector'){
                                    insert_dict[guys_id] = all_els[r].value.trim();
                                }
                            }
                            person_selector = top_el.getElementById('person_selector');
                            person = person_selector.value;
                            person_sk = '';
                            is_external = true;
                            attempted_name = ''
                            has_login = top_el.getElementById('has_login').getAttribute('checked');
                            had_login = top_el.getElementById('has_login').getAttribute('extra1');
                            existing_login_name = top_el.getElementById('has_login').getAttribute('extra2');
                            person_obj = null;
                            is_employee = top_el.getElementById('is_employee').getAttribute('checked');
                            was_employee = top_el.getElementById('is_employee').getAttribute('extra1');
                            ret_dict = {'login': '', 'pass': ''};
                            if(person != 'NEW'){
                                person_sk = server.build_search_key('twog/person', person)
                                server.update(person_sk, insert_dict);
                                person_obj = server.eval("@SOBJECT(twog/person['code','" + person + "'])")[0];
                                if(is_employee == 'true' && was_employee == 'false'){
                                    ret_dict = create_login(insert_dict, person_obj, 'internal', 'user');
                                }else if(has_login == 'true' && had_login == 'false' && is_employee == 'false'){
                                    ret_dict = create_login(insert_dict, person_obj, 'external', 'user');
                                }
                            }else{
                                new_person = server.insert('twog/person',insert_dict);
                                person_obj = new_person;
                                person = new_person.code;
                                person_sk = new_person.__search_key__;
                                if(has_login == 'true'){
                                    loc = 'external';
                                    if(is_employee == 'true'){
                                        is_external = false;
                                        loc = 'internal';
                                    } 
                                    ret_dict = create_login(insert_dict, person_obj, loc, 'user');
                                }
                            }  
                            if(ret_dict['login'] != ''){
                                existing_login_name = ret_dict['login'];
                            }
                            //Need to link person and login to client and company
                            // See if they are linked to another place first. If this has changed, remove the old entries or change them, then make the new ones
                            linked_to_client = false;
                            company = top_el.getElementById('company_code').value;
                            company_name = '';
                            if(company != '' && company != null && company != '--Select--' && is_external && has_login == 'true'){
                                company_obj = server.eval("@SOBJECT(twog/company['code','" + company + "'])")
                                if(company_obj.length > 0){
                                    client_code = company_obj[0].client_code;
                                    company_name = company_obj[0].name;
                                    if(client_code != '' && client_code != null){
                                        client = server.eval("@SOBJECT(twog/client['code','" + client_code + "'])");
                                        if(client.length > 0){
                                            server.update(person_sk, {'client_code': client_code});
                                            linked_to_client = true;
                                        }
                                    }else{
                                        if(confirm("Company '" + company_name + "' is not attached to any client. Would you like to make '" + company_name + "' a client as well?")){
                                            exists2 = server.eval("@SOBJECT(twog/client['name','" + company_name + "'])");
                                            if(exists2.length == 0){
                                                new_client = server.insert('twog/client', {'name': company_name, 'billing_status': 'No Billing Problems'});
                                                server.update(company_obj[0].__search_key__, {'client_code': new_client.code});
                                                attempted_login = replaceAll(' ','',company_name.toLowerCase());
                                                if(attempted_login.length > 5){
                                                    attempted_login = attempted_login.substr(0,5);
                                                }
                                                attempted_login = 'gg_' + attempted_login;
                                                login_inserted = false;
                                                while(!login_inserted){
                                                    random_num = getRandomInt(100, 999);
                                                    attempted_login = attempted_login + String(random_num);
                                                    anyofem = server.eval("@SOBJECT(sthpw/login['login','" + attempted_login + "'])");
                                                    if(anyofem.length == 0){
                                                        english_pass = reverse(attempted_login) + String(getRandomInt(100, 999)); 
                                                        passwo = spt.md5(english_pass); 
                                                        server.insert('twog/person', {'login_name': attempted_login, 'first_name': company_name, 'last_name': 'Portal Account', 'email': 'portal.account@2gdigital.com', 'client_code': new_client.code, 'company_code': company_obj[0].code});
                                                        server.insert('sthpw/login', {'login': attempted_login, 'code': attempted_login, 'first_name': company_name, 'last_name': 'Portal Account', 'password': passwo, 'license_type': 'user', 'email': 'portal.account@2gdigital.com', 'display_name': 'Portal Account, ' + company_name, 'location': 'external'});
                                                        server.insert('sthpw/login_in_group', {'login_group': 'client', 'login': attempted_login});
                                                        server.update(new_client.__search_key__, {'portal_login': attempted_login, 'portal_pass': english_pass});
                                                        login_inserted = true;
                                                        linked_to_client = true;
                                                    }
                                                }
                                                
                                            }else{
                                                alert("A Client with the name " + company_name + " already exists.");
                                            }
                                        }
                                    } 
                                }
                            }
                            if(!linked_to_client && is_external && has_login == 'true'){
                                alert("This user is not linked to any client, as the Company and Client objects are not linked.")
                            }
                            if(has_login == 'true'){
                                person_obj = server.eval("@SOBJECT(twog/person['code','" + person_obj.code + "'])")[0];
                                logn = person_obj.login_name;
                                linked_login = null;
                                if(logn != '' && logn != null){
                                    linked_login = server.eval("@SOBJECT(sthpw/login['login','" + logn + "'])");
                                }
                                if(linked_login.length > 0){
                                    linked_login = linked_login[0];
                                    disab = top_el.getElementById('account_disabled').getAttribute('checked');
                                    if(disab == 'true'){
                                        server.update(linked_login.__search_key__, {'license_type': 'disabled'});
                                    }else{
                                        server.update(linked_login.__search_key__, {'license_type': 'user'});
                                    }
                                }
                            }
                            if(is_employee == 'true'){
                                //Then make the groups match what was selected
                                group_checks = top_el.getElementsByClassName('group_check');
                                for(var r = 0; r < group_checks.length; r++){
                                    is_selected = group_checks[r].getAttribute('checked');
                                    was_already = group_checks[r].getAttribute('extra1');
                                    group_name = group_checks[r].getAttribute('value_field'); 
                                    if(is_selected == 'true' && was_already == 'false'){
                                        //Then add them to the group
                                        server.insert('sthpw/login_in_group', {'login': existing_login_name, 'login_group': group_name});
                                    }else if(is_selected == 'false' && was_already == 'true'){
                                        //Then remove them from the group
                                        grouper = server.eval("@SOBJECT(sthpw/login_in_group['login','" + existing_login_name + "']['login_group','" + group_name + "'])");
                                        if(grouper.length > 0){
                                            grouper = grouper[0];
                                            server.retire_sobject(grouper.__search_key__);
                                        }
                                    }
                                }
                            } 
                            kwargs = {'person_code': person};
                            if(ret_dict['login'] != ''){
                                kwargs['login_name'] = ret_dict['login'];
                                kwargs['login_pass'] = ret_dict['pass'];
                            }
                            spt.api.load_panel(top_el, 'login_manager.LoginManagerWdg', kwargs);
                            
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def switch_has_login(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var top_el = spt.api.get_parent(bvr.src_el, '.login_manager_wdg');
                          has_login = top_el.getElementById('has_login');
                          group_row = top_el.getElementById('group_row');
                          if(bvr.src_el.getAttribute('checked') == 'true'){
                              has_login.setAttribute('checked','true');
                              has_login.innerHTML = bvr.src_el.innerHTML;
                              group_row.style.display = 'table-row';
                          }else{
                              group_row.style.display = 'none';
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior
      
    def get_snapshot(my, person, login=None):
        path = '/context/icons/common/no_image.png'
        if person:
            from tactic_client_lib import TacticServerStub
            server = TacticServerStub.get() 
            snapshot = server.get_snapshot(person, context="MISC")
            print "SNAPSHOT = %s" % snapshot
            if not snapshot:
                print "NO SNAPSHOT"
                if login:
                    snapshot = server.get_snapshot(login, context="icon")
                    print "SNAPSHOT = %s" % snapshot
            #['lib', 'client_repo', 'sandbox', 'local_repo', 'web', 'relative']
            if snapshot:
                path = server.get_path_from_snapshot(snapshot.get('code'), file_type="main", mode="web")     
        img = '''<img height="80px" src="%s"/>''' % path
        return img

    def txtbox(my, name, val, width='200px'):
        txt = TextWdg(name)
        txt.add_attr('id',name)
        txt.add_style('width: %s;' % width)
        txt.set_value(val)
        return txt

    def get_display(my):
        person_code = ''
        person = None
        person_exists = False
        has_login = 'false'
        is_disabled = 'false'
        is_employee = 'false'
        login_obj = None
        password = ''
        existing_login_name = ''
        if 'person_code' in my.kwargs.keys():
            person_code = my.kwargs.get('person_code')
            person_s = Search("twog/person")
            person_s.add_filter('code',person_code)
            person = person_s.get_sobject()
            if person:
                person_exists = True
                login_name = person.get_value('login_name')
                if login_name not in [None,'']:
                    login_s = Search("sthpw/login")
                    login_s.add_filter('login',login_name)
                    login_obj = login_s.get_sobject()
                    if login_obj:
                        has_login = 'true'
                        license_type = login_obj.get_value('license_type')
                        password = login_obj.get_value('password')
                        existing_login_name = login_obj.get_value('login')
                        if license_type == 'disabled':
                            is_disabled = 'true'
                        if login_obj.get_value('location') == 'internal':
                            is_employee = 'true'
        first_name = ''
        last_name = ''
        company_code = ''
        title = ''
        email = ''
        alternate_email = ''
        main_phone = ''
        work_phone = ''
        cell_phone = ''
        home_phone = ''
        fax = ''
        country = ''
        state = ''
        city = ''
        zip = ''
        street_address = ''
        suite = ''
        if person_exists:
            first_name = person.get_value('first_name')
            last_name = person.get_value('last_name')
            company_code = person.get_value('company_code')
            title = person.get_value('title')
            email = person.get_value('email')
            alternate_email = person.get_value('alternate_email')
            main_phone = person.get_value('main_phone')
            work_phone = person.get_value('work_phone')
            cell_phone = person.get_value('cell_phone')
            home_phone = person.get_value('home_phone')
            fax = person.get_value('fax')
            country = person.get_value('country')
            state = person.get_value('state')
            city = person.get_value('city')
            zip = person.get_value('zip')
            street_address = person.get_value('street_address')
            suite = person.get_value('suite')

        people_s = Search("twog/person")
        people_s.add_order_by('last_name')
        people_s.add_order_by('first_name')
        people = people_s.get_sobjects()
        peep_sel = SelectWdg("person_selector")
        peep_sel.add_attr('id','person_selector')
        peep_sel.append_option('--Create New Login--','NEW')
        for peep in people:
            peep_sel.append_option('%s, %s' % (peep.get_value('last_name'), peep.get_value('first_name')), peep.get_code())
        if person_exists:
            peep_sel.set_value(person_code)
        peep_sel.add_behavior(my.switch_person())

        company_s = Search("twog/company")
        company_s.add_order_by('name')
        companies = company_s.get_sobjects()
        comp_sel = SelectWdg('company_code')
        comp_sel.add_attr('id','company_code')
        comp_sel.append_option('--Select--','')
        for company in companies:
            comp_sel.append_option(company.get_value('name'), company.get_code())
        if person_exists:
            comp_sel.set_value(company_code)
        
        country_sel = SelectWdg('country')
        country_sel.add_attr('id','country')
        country_sel.append_option('--Select--','')
        for country in my.countries:
            country_sel.append_option(country,country)
        if person_exists:
            my_country = person.get_value('country')
            if my_country in [None,'']:
                my_country = ''
            country_sel.set_value(my_country)

        state_sel = SelectWdg('state')
        state_sel.add_attr('id','state')
        state_sel.append_option('--Select--','')
        for state in my.states:
            state_sel.append_option(state,state)
        if person_exists:
            my_state = person.get_value('state')
            if my_state in [None,'']:
                my_state = ''
            state_sel.set_value(my_state)

        group_tbl = Table()
        group_tbl.add_row()
        group_tbl.add_cell("<b><u>GROUPS:</u></b>")
        login_gs = Search('sthpw/login_group')
        login_gs.add_order_by('login_group')
        login_groups = login_gs.get_sobjects()
        lgs = []
        if has_login == 'true':
            my_lg_s = Search('sthpw/login_in_group')
            my_lg_s.add_filter('login',login_obj.get_value('login'))
            my_lgs = my_lg_s.get_sobjects()
            for ml in my_lgs:
                lgs.append(ml.get_value('login_group'))
        group_tbl.add_row()
        lcount = 0
        for lg in login_groups:
            if lg.get_value('login_group') not in ['client','user','default']:
                if lcount % 7 == 0:
                    group_tbl.add_row()
                this_group = 'false'
                if lg.get_value('login_group') in lgs:
                    this_group = 'true'
                chk = CustomCheckboxWdg(name='group_check_%s' % lcount,value_field=lg.get_value('login_group'),id='group_check_%s' % lcount,checked=this_group,dom_class='group_check',text='%s:' % lg.get_value('login_group').upper(),text_spot='right',text_align='left',nowrap='nowrap',extra1=this_group) 
                group_tbl.add_cell(chk)
                lcount = lcount + 1
        group_tbl.add_row()
        group_tbl.add_cell('&nbsp;')
                

        widget = DivWdg()
        table = Table()
        table.add_attr('class','login_manager_wdg')
        lt = Table()
        ltop = Table()
        red_row = ltop.add_row()
        red_row.add_attr('id','red_row')
        red_row.add_style('background-color: #FF0000;')
        if 'login_name' in my.kwargs.keys():
            ltop.add_cell("<b>Login Name: %s, Password: %s</b>" % (my.kwargs.get('login_name'), my.kwargs.get('login_pass'))) 
        else:
            red_row.add_style('display: none;')
        ltop.add_row()
        emp_checker = CustomCheckboxWdg(name='is_employee',value_field='is_employee',id='is_employee',checked=is_employee,dom_class='is_employee',additional_js=my.switch_has_login(),extra1=is_employee) 
        ltop.add_cell(emp_checker)
        ltop.add_cell('Is Employee?')
        ltop.add_cell('&nbsp;&nbsp;&nbsp;')
        login_checker = CustomCheckboxWdg(name='has_login',value_field='has_login',id='has_login',checked=has_login,dom_class='has_login',extra1=has_login,extra2=existing_login_name) 
        ltop.add_cell(login_checker)
        ltop.add_cell('Enable Login?')
        ltop.add_cell('&nbsp;&nbsp;&nbsp;')
        disabled_checker = CustomCheckboxWdg(name='account_disabled',value_field='account_disabled',id='account_disabled',checked=is_disabled,dom_class='account_disabled',extra1=is_disabled) 
        ltop.add_cell(disabled_checker)
        ltop.add_cell('Account Disabled?')
        group_row = ltop.add_row()
        group_row.add_attr('id','group_row')
        if is_employee != 'true':
            group_row.add_style('display: none;')
        gcell = ltop.add_cell(group_tbl)
        gcell.add_attr('colspan','7')
        
        lt.add_row()
        ltt = lt.add_cell(ltop)
        ltt.add_attr('colspan','2')
  
        lt.add_row() 
        lt.add_cell('First Name: ')
        lt.add_cell(my.txtbox('first_name',first_name))
        lt.add_row() 
        lt.add_cell('Last Name: ')
        lt.add_cell(my.txtbox('last_name',last_name))
        lt.add_row()
        lt.add_cell('Company: ')
        side_tbl = Table()
        side_tbl.add_row()
        side_tbl.add_cell(comp_sel)
        side_tbl.add_cell("&nbsp;&nbsp;&nbsp;&nbsp;")
        add_comp = side_tbl.add_cell('<input type="button" value="Add New Company"/>')
        add_comp.add_behavior(my.add_company())
        lt.add_cell(side_tbl)
        lt.add_row() 
        lt.add_cell('Title: ')
        lt.add_cell(my.txtbox('title',title))
        lt.add_row() 
        lt.add_cell('Email: ')
        lt.add_cell(my.txtbox('email',email))
        lt.add_row() 
        lt.add_cell('Alt Email: ')
        lt.add_cell(my.txtbox('alternate_email',alternate_email))
        lt.add_row() 
        lt.add_cell('Main Phone: ')
        lt.add_cell(my.txtbox('main_phone',main_phone))
        lt.add_row() 
        lt.add_cell('Work Phone: ')
        lt.add_cell(my.txtbox('work_phone',work_phone))
        lt.add_row() 
        lt.add_cell('Cell Phone: ')
        lt.add_cell(my.txtbox('cell_phone',cell_phone))
        lt.add_row() 
        lt.add_cell('Home Phone: ')
        lt.add_cell(my.txtbox('home_phone',home_phone))
        lt.add_row() 
        lt.add_cell('Fax: ')
        lt.add_cell(my.txtbox('fax',fax))
        lt.add_row() 
        lt.add_cell('Country: ')
        lt.add_cell(country_sel)
        lt.add_row() 
        lt.add_cell('State: ')
        lt.add_cell(state_sel)
        lt.add_row() 
        lt.add_cell('City: ')
        lt.add_cell(my.txtbox('city',city))
        lt.add_row() 
        lt.add_cell('Zip: ')
        lt.add_cell(my.txtbox('zip',zip))
        lt.add_row() 
        lt.add_cell('Street Address: ')
        lt.add_cell(my.txtbox('street_address',street_address))
        lt.add_row() 
        lt.add_cell('Suite: ')
        lt.add_cell(my.txtbox('suite',suite))

        img = my.get_snapshot(person, login_obj) 

        rt = Table()
        rt.add_attr('width','300px')
        rt.add_style('background-color: #ba4e33;')
        rt.add_style('height: 400px;')
        rt.add_row()
        img_cell = rt.add_cell(img)
        img_cell.add_attr('valign','top')
        img_cell.add_attr('align','center')

        selector_row = table.add_row()
        selector_row.add_attr('id','selector_row')
        select_tbl = Table()
        select_tbl.add_row()
        select_tbl.add_cell('Person: ')
        select_tbl.add_cell(peep_sel)

        select_cell = table.add_cell(select_tbl)
        select_cell.add_attr('colspan','3')
        select_cell.add_attr('align','center') 
        table.add_row()
        top1 = table.add_cell(lt)
        top1.add_attr('valign','top')
        table.add_cell('&nbsp;&nbsp;&nbsp;&nbsp;') 
        top2 = table.add_cell(rt)
        top2.add_attr('valign','top')
        table.add_row()
        save_butt = table.add_cell('<input type="button" value="Save/Create" />')
        save_butt.add_attr('colspan','3')
        save_butt.add_attr('align','center')
        save_butt.add_behavior(my.get_save())
        widget.add(table)
        return widget
        
        
        
