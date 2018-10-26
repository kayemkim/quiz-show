from flask import Flask, render_template, flash, g
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
from flask import request
import flask_sijax
import random


qa_set = {
    0:(
        '''이순신(李舜臣, 1545년 4월 28일 ~ 1598년 12월 16일 (음력 11월 19일))은 조선 중기의 무신이다. 본관은 덕수(德水), 자는 여해(汝諧), 시호는 충무(忠武)이며, 한성 출신이다. 문반 가문 출신으로 1576년(선조 9년) 무과(武科)에 급제[2]하여 그 관직이 동구비보 권관, 훈련원 봉사, 발포진 수군만호, 조산보 만호, 전라좌도 수군절도사를 거쳐 정헌대부 삼도수군통제사에 이르렀다. 함경도 동구비보권관(董仇非堡權管), 1581년 발포 수군만호(鉢浦水軍萬戶)가 되었다가 전라좌수영의 오동나무를 베기를 거절한 일로 좌수사 성박의 미움을 받기도 했다. 이후 1583년 남병사의 군관과 건원보권관, 훈련원참군, 1586년 사복시주부를 거쳐 조산보만호 겸 녹도둔전사의(造山堡萬戶兼鹿島屯田事宜)로 부임했다. 조산만호 겸 녹둔도사의 재직 중 1587년(선조 20년) 9월의 여진족의 사전 기습공격으로 벌어진 녹둔도전투에서 패하여, 북병사 이일의 탄핵을 받고 백의종군(白衣從軍)하는 위치에 서기도 했다.''',
        '이순신이 태어난 곳은?',
        '한양', 
        0.9),
    1:(
        '''조선 세종(朝鮮 世宗, 1397년 5월 15일[1] (음력 4월 10일) ~ 1450년 3월 30일 (음력 2월 17일), 재위 1418년 ~ 1450년)은 조선의 제4대 군주이며 언어학자이다. 그의 업적에 대한 존경의 의미를 담은 명칭인 세종대왕(世宗大王)으로 자주 일컬어진다. 성은 이(李), 휘는 도(祹), 본관은 전주(全州), 자는 원정(元正), 아명은 막동(莫同)이다. 세종은 묘호이며, 시호는 영문예무인성명효대왕(英文睿武仁聖明孝大王)이고, 명나라에서 받은 시호는 장헌(莊憲)이다. 존시를 합치면 세종장헌영문예무인성명효대왕(世宗莊憲英文睿武仁聖明孝大王)이 된다.''',
        '세종대왕은 조선의 몇 대 왕인가?', 
        '4대',
        0.7),
    2:(
        '''이순신(李舜臣, 1545년 4월 28일 ~ 1598년 12월 16일 (음력 11월 19일))은 조선 중기의 무신이다. 본관은 덕수(德水), 자는 여해(汝諧), 시호는 충무(忠武)이며, 한성 출신이다. 문반 가문 출신으로 1576년(선조 9년) 무과(武科)에 급제[2]하여 그 관직이 동구비보 권관, 훈련원 봉사, 발포진 수군만호, 조산보 만호, 전라좌도 수군절도사를 거쳐 정헌대부 삼도수군통제사에 이르렀다. 함경도 동구비보권관(董仇非堡權管), 1581년 발포 수군만호(鉢浦水軍萬戶)가 되었다가 전라좌수영의 오동나무를 베기를 거절한 일로 좌수사 성박의 미움을 받기도 했다. 이후 1583년 남병사의 군관과 건원보권관, 훈련원참군, 1586년 사복시주부를 거쳐 조산보만호 겸 녹도둔전사의(造山堡萬戶兼鹿島屯田事宜)로 부임했다. 조산만호 겸 녹둔도사의 재직 중 1587년(선조 20년) 9월의 여진족의 사전 기습공격으로 벌어진 녹둔도전투에서 패하여, 북병사 이일의 탄핵을 받고 백의종군(白衣從軍)하는 위치에 서기도 했다.''',
        '이순신이 태어난 곳은?',
        '한양', 
        0.9),
    3:(
        '''조선 세종(朝鮮 世宗, 1397년 5월 15일[1] (음력 4월 10일) ~ 1450년 3월 30일 (음력 2월 17일), 재위 1418년 ~ 1450년)은 조선의 제4대 군주이며 언어학자이다. 그의 업적에 대한 존경의 의미를 담은 명칭인 세종대왕(世宗大王)으로 자주 일컬어진다. 성은 이(李), 휘는 도(祹), 본관은 전주(全州), 자는 원정(元正), 아명은 막동(莫同)이다. 세종은 묘호이며, 시호는 영문예무인성명효대왕(英文睿武仁聖明孝大王)이고, 명나라에서 받은 시호는 장헌(莊憲)이다. 존시를 합치면 세종장헌영문예무인성명효대왕(世宗莊憲英文睿武仁聖明孝大王)이 된다.''',
        '세종대왕은 조선의 몇 대 왕인가?', 
        '4대',
        0.7)
}

# straight from the wtforms docs:
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code = IntegerField('Area Code/Exchange', [validators.required()])
    number = TextField('Number')


class ExampleForm(Form):
    field1 = TextField('First Field', description='This is field one.')
    field2 = TextField('Second Field', description='This is field two.',
                       validators=[Required()])
    hidden_field = HiddenField('You cannot see this', description='Nope')
    recaptcha = RecaptchaField('A sample recaptcha field')
    radio_field = RadioField('This is a radio field', choices=[
        ('head_radio', 'Head radio'),
        ('radio_76fm', "Radio '76 FM"),
        ('lips_106', 'Lips 106'),
        ('wctr', 'WCTR'),
    ])
    checkbox_field = BooleanField('This is a checkbox',
                                  description='Checkboxes can be tricky.')

    # subforms
    mobile_phone = FormField(TelephoneForm)

    # you can change the label as well
    office_phone = FormField(TelephoneForm, label='Your office phone')

    ff = FileField('Sample upload')

    submit_button = SubmitField('Submit Form')


    def validate_hidden_field(form, field):
        raise ValidationError('Always wrong')


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    @app.route('/', methods=('GET', 'POST'))
    def index():
        form = ExampleForm()
        form.validate_on_submit()  # to get error messages to the browser
        flash('critical message', 'critical')
        flash('error message', 'error')
        flash('warning message', 'warning')
        flash('info message', 'info')
        flash('debug message', 'debug')
        flash('different message', 'different')
        flash('uncategorized message')
        return render_template('index.html', form=form)

    return app

def create_app_new(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)
    flask_sijax.Sijax(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    @app.route('/', methods=('GET', 'POST'))
    def index():
        form = ExampleForm()
        form.validate_on_submit()  # to get error messages to the browser
        flash('critical message', 'critical')
        flash('error message', 'error')
        flash('warning message', 'warning')
        flash('info message', 'info')
        flash('debug message', 'debug')
        flash('different message', 'different')
        flash('uncategorized message')
        return render_template('index.html', form=form)

    @app.route('/quiz')
    def quiz():
        qid = random.sample(range(len(qa_set.keys())), 1)[0]
        contents, question, answer, score = qa_set[qid]



        # product = PRODUCTS.get(key)
        # if not product:
        #     abort(404)
        #return render_template('quiz.html', product=product)

        return render_template('quiz.html', contents=contents, qid=qid, question=question)

    # @flask_sijax.route(app, '/result')
    @app.route('/result', methods=['POST'])
    def result():
        # Every Sijax handler function (like this one) receives at least
        # one parameter automatically, much like Python passes `self`
        # to object methods.
        # The `obj_response` parameter is the function's way of talking
        # back to the browser
        # def say_hi(obj_response):
        #     obj_response.alert('Hi there!')

        qid = request.form['qid']
        answer = request.form['answer']

        correct_answer = qa_set[int(qid)][2]
        result_message = ''
        animation = ''

        if correct_answer == answer:
            result_message = '정답이에요~';
            animation = 'pulse slow';
        else:
            result_message = '땡! 기계보다 못한..'
            animation = 'hinge delay-2s';
        
        
        # if g.sijax.is_sijax_request:
        #     # Sijax request detected - let Sijax handle it
        #     g.sijax.register_callback('say_hi', say_hi)
        #     return g.sijax.process_request()

        # Regular (non-Sijax request) - render the page template
        return render_template('result.html', 
            result_message=result_message,
            correct_answer=correct_answer,
            animation=animation)


    return app

if __name__ == '__main__':
    create_app_new().run(debug=True)
