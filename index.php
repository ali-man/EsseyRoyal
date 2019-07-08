<?php
use yii\bootstrap\ActiveForm;
use yii\helpers\Url;
    $this->title = "Essay Royal";
?>
<!-- HEADER -->
<section id="home-section" class="header-bg">
    <div class="gradient sectionP60 header-pad">
        <div class="container">
            <div class="row">
                <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="row">
                        <div class="col-md-5 col-sm-5 col-xs-12 header-text sectionP60">
                            <h1 class="rL white">Need write an essay?</h1>
                            <h1 class="rL white">Make it happen!</h1>
                            <p class="rL blue-L">We are providing professional writing service by the cheapest rates in a shortest deadlines. </p>
                            <a href="<?= (Yii::$app->user->isGuest) ? '#calc-section' : Url::to(['package/index']) ?>" class="btn btn-gradient" data-aos="zoom-in-up" data-aos-duration="800"><?= (Yii::$app->user->isGuest) ? 'Calculation' : 'Dashboard' ?></a>
                        </div>
                        <div class="col-md-6 col-sm-6 col-xs-12 pull-right">
                            <div class="login-div centered" data-aos="fade-up" data-aos-duration="1000">
                                <div class="head">
                                    <h3 class="purple oR m0"><?= (Yii::$app->user->isGuest) ? 'LOGIN' : 'WELCOME!' ?></h3>
                                    <p class="light oR">
                                        <?= (Yii::$app->user->isGuest) ? 'Enter your credentials to login.' : 'You are logged!' ?>
                                    </p>
                                </div>
                                <?php if(Yii::$app->user->isGuest): ?>
                                <?php $form = ActiveForm::begin(['id'=>'login-form', 'action'=>'/login']); ?>
                                    <div class="body">
                                        <div class="input-box">
                                            <input placeholder="Email" name="LoginForm[username]" type="text" required>
                                            <span style="position: absolute"><i class="fa fa-user"></i></span>
                                        </div>
                                        <div class="input-box">
                                            <input placeholder="Password" name="LoginForm[password]" type="password" required>
                                            <span style="position: absolute"><i class="fa fa-key"></i></span>
                                        </div>
                                        <div style="display: none;margin-top:5px;margin-bottom:-35px;" id="error-list-login" class="alert alert-danger" role="alert"></div>
                                    </div>
                                    <div class="foot">
                                        <a href="#" data-toggle="modal" data-target="#pop-register" class="forgot pull-left"><small>Register</small></a>
                                        <button type="submit" class="btn btn-gradient W100 pull-right" data-aos="zoom-in-up" data-aos-duration="800">Login!</button>
                                    </div>
                                <?php ActiveForm::end(); ?>
                                <?php else: ?>
                                    <div class="body text-center" style="margin-top: 15px;padding-top: 20px; margin-bottom: 20px">
                                        <img style="box-shadow: 0px 0px 5px 4px #ff6f0e5c;" src="<?=Yii::$app->user->identity->photo?>" class="img-circle" width="150px" alt="">
                                        <h3><?=Yii::$app->user->identity->first_name?></h3>
                                    </div>
                                    <div class="foot">
                                        <a href="<?=Url::to(['site/logout'])?>" class="forgot pull-left"><small><i class="fa fa-sign-out"></i> Logout</small></a>
                                        <a href="<?=Url::to(['package/index'])?>" class="btn btn-gradient W100 pull-right" data-aos="zoom-in-up" data-aos-duration="800">Dashboard</a>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- HEADER -->

<!-- About -->
<section id="calc-section" class="grey-bg" style="padding-bottom: 60px;">
    <div class="container">
        <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="services-div margin-minus" data-aos="fade-up" data-aos-duration="1000">
                    <div class="col-md-3 col-sm-6 col-xs-12 text-center br service-hover">
                        <div class="service" data-aos="zoom-in" data-aos-duration="1000">
                            <div class="service-icon">
                                <i class="fa fa-puzzle-piece"></i>
                            </div>
                            <div class="service-desc">
                                <h4 class="blue oB">There is no problem</h4>
                                <p class="light oR">That we couldn't solve, you know. And that is our priority to solve your problems great! </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6 col-xs-12 text-center br b0 service-hover">
                        <div class="service" data-aos="zoom-in" data-aos-duration="1000">
                            <div class="service-icon">
                                <i class="fa fa-paint-brush"></i>
                            </div>
                            <div class="service-desc">
                                <h4 class="blue oB">Unique & creative</h4>
                                <p class="light oR">We guarantee the uniqueness of each word and sentence. Still do not believe in it?</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6 col-xs-12 text-center br b0 service-hover">
                        <div class="service" data-aos="zoom-in" data-aos-duration="1000">
                            <div class="service-icon">
                                <i class="fa fa-hourglass-2"></i>
                            </div>
                            <div class="service-desc">
                                <h4 class="blue oB">Reach your goals</h4>
                                <p class="light oR">Let us make your paper job, our extreme professional writers will take care of it</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6 col-xs-12 text-center br service-hover">
                        <div class="service" data-aos="zoom-in" data-aos-duration="1000">
                            <div class="service-icon">
                                <i class="fa fa-dollar"></i>
                            </div>
                            <div class="service-desc">
                                <h4 class="blue oB">Risk Free</h4>
                                <p class="light oR">We provide complete money back guarantee, take a look in FAQ for more information</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12 text-center">
                <div id="wwa">
                    <div class="heading-text" data-aos="fade-up" data-aos-duration="1000">
                        <span class="gold-gradient-color">Calculate your order</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- About -->
<section class="counter-bg">
    <div class="sectionP40 blue-bg">
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <?php $form = \yii\widgets\ActiveForm::begin(['method'=>'GET', 'action'=> '/package/create'])?>
                    <div class="col-md-6 col-md-offset-0 col-sm-10 col-sm-offset-1 col-xs-12">
                        <div class="responsive" data-aos="fade-right" data-aos-duration="1000">
                            <div>
                                <div class="row">
                                    <div class="col-lg-12">
                                        <div class="form-group">
                                            <select id="package-pages" class="form-control btn-gradient calc-select-style" name="pages">
                                                <?php foreach(\app\models\Package::pageList() as $key=>$value): ?>
                                                  <option value="<?=$key?>"><?=$value?></option>
                                                <?php endforeach; ?>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-lg-12">
                                        <div class="form-group">
                                            <select class="form-control btn-gradient calc-select-style">
                                                <?php foreach(\app\models\SubjectArea::find()->all() as $item): ?>
                                                  <option value="<?=$item->id?>"><?=$item->name?></option>
                                                <?php endforeach; ?>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-lg-12">
                                        <div class="form-group">
                                            <select name="deadline_id" id="package-deadline_id" class="form-control btn-gradient calc-select-style calc-select">
                                                <?php foreach(\app\models\Deadline::find()->all() as $item): ?>
                                                  <option value="<?=$item->id?>"><?=$item->name?></option>
                                                <?php endforeach; ?>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-lg-12">
                                        <div class="form-group">
                                            <select name="al_id" id="package-al_id" class="form-control btn-gradient calc-select-style calc-select">
                                              <?php foreach(\app\models\AcademicLevel::find()->all() as $item): ?>
                                                <option value="<?=$item->id?>"><?=$item->name?></option>
                                              <?php endforeach; ?>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="counter" class="col-md-5 col-sm-12 col-xs-12 pull-right resPad0">
                        <div class="col-md-6 col-sm-3 col-xs-6 br bb">
                            <div class="numbers text-center" data-aos="zoom-in" data-aos-duration="1000">
                                <span class="numscroller rB gold-gradient-color" id="per-page"></span>
                                <p class="white oR">Per page</p>
                            </div>
                        </div>
                        <div class="col-md-6 col-sm-3 col-xs-6 bb">
                            <div class="numbers text-center" data-aos="zoom-in" data-aos-duration="1000">
                                <span id="price-body" class="numscroller rB gold-gradient-color"></span>
                                <p class="white oR">Total cost</p>
                            </div>
                        </div>
                        <div class="col-md-6 col-sm-3 col-xs-6 br">
                            <button style="margin-top:20px" class="btn btn-gradient  W100 pull-right aos-init" data-aos="zoom-in-up" data-aos-duration="1800">Request to order</button>
                        </div>
                        <div class="col-md-6 col-sm-3 col-xs-6">

                        </div>
                    </div>
                    <?php \yii\widgets\ActiveForm::end()?>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Why Choose Us -->
<section id="why-us-section" class="sectionP60">
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <div class="col-md-5 col-md-offset-0 col-sm-10 col-sm-offset-1 col-xs-12">
                    <div class="responsive rsb"  data-aos="fade-right" data-aos-duration="1000">
                        <div class="heading-text">
                            <span class="blue-gradient-color">Why Us?</span>
                        </div>
                        <p class="light oR text-justify">Essay writing is a critical job that demands skills and knowledge. Hire professionals to help you with remarkable paper writing and achieve better credits.</p>
                        <br>
                        <p class="light oR text-justify">
                            Often essays are the toughest part of the curriculum to deal with, our essay writing services ensure that no student lacks behind because of the poor score in essay writing. We offer affordable essay writing services in all subjects to help students achieve better grades.
                        </p>
                    </div>
                </div>
                <div class="col-md-5 col-md-offset-1 col-sm-10 col-sm-offset-1 col-xs-12">
                    <div class="video-embed pull-right" data-aos="fade-left" data-aos-duration="1000">
                        <div class="thumb">
                            <span><img src="/assets/front/images/logo.png" alt=""></span>
                        </div>
                        <iframe width="533" height="300" src="" frameborder="0" allowfullscreen></iframe>
                        <!--<iframe src="https://player.vimeo.com/video/202406936?title=0&amp;byline=0&amp;portrait=0&amp;color=FDA10E&amp;autoplay=0" width="100%" height="300" autoplay="0" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></iframe>-->
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- Why Choose Us -->

<!-- How We Work -->
<section id="how-section" class="sectionP60 grey-bg">
    <div class="container">
        <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="col-md-12 col-md-offset-0 col-sm-12 col-xs-12">
                    <div data-aos="fade-right" data-aos-duration="1000">
                        <div class="heading-text">
                            <span class="blue-gradient-color">Why Essay Royal?</span>
                        </div>
                        <p class="light rL" style="font-size: 16px;">
                            If you are struggling with essays and want professional help, Essay Royal is your one point solution for all problems. We are a leading essay writing services provider offering high-quality, error-free and affordable content. You must hire us to take advantage of:
                        </p>
                    </div>
                </div>
                <div class="col-md-12 col-sm-12 col-xs-12 p0 sectionP40">
                    <div class="col-md-4 col-sm-12 col-xs-12">
                        <div class="service2" data-aos="zoom-in" data-aos-duration="1000">
                            <div class="service2-icon">
                                <i class="gold-gradient-color fa fa-lightbulb-o"></i>
                            </div>
                            <div class="service2-desc">
                                <h4 class="blue oB">Plagiarism Free Content</h4>
                                <p class="light oR text-justify">
                                    Plagiarism is the biggest problem to deal with while writing an essay. While you can knowingly or unknowingly copy someone else’s work, hiring professionals allows you to prevent this error. A professional essay writer understands the importance of plagiarism free content and offers you 100% original and unique content.
                                    With our skills and knowledge, we have achieved 100% success rate in hiring original content and assure that the content is genuine to the highest level.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 col-sm-12 col-xs-12">
                        <div class="service2" data-aos="zoom-in" data-aos-duration="1000">
                            <div class="service2-icon">
                                <i class="gold-gradient-color fa fa-send-o"></i>
                            </div>
                            <div class="service2-desc">
                                <h4 class="blue oB">Instant Delivery</h4>
                                <p class="light oR text-justify">
                                    Got an urgent essay project, we are readily available to serve you in a jiffy. Our instant delivery system helps students get an essay delivered in as short as 60 minutes. On regular basis, it takes us 8 hours to fetch you the best results, but, in case of urgency, we cater to your requirement with the best quality content in just 60 minutes.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 col-sm-12 col-xs-12">
                        <div class="service2" data-aos="zoom-in" data-aos-duration="1000">
                            <div class="service2-icon">
                                <i class="gold-gradient-color fa fa-lock"></i>
                            </div>
                            <div class="service2-desc">
                                <h4 class="blue oB">Secure Payments</h4>
                                <p class="light oR text-justify">
                                    While most of the platforms demand upfront payments, we allow our clients to pay once they are satisfied with the quality of work. We request you to review the essay or part of it, as you receive it and once satisfied; pay us for our hard work.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- How We Work -->


<!-- What Can We Offer -->
<section id="offers-section" class="hiw-bg">
    <div class="sectionP60 grey-bg-o">
        <div class="container">
            <div class="row">
                <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="col-md-8 col-md-offset-2 col-sm-10 col-sm-offset-1 col-xs-12 text-center">
                        <div data-aos="fade-up" data-aos-duration="1000">
                            <div class="heading-text">
                                <span class="gold-gradient-color">What we can offer?</span>
                            </div>
                            <p class="light oR" style="font-size: 16px;">
                                Unlike others, we aren’t chasing quantity but we aim to cater to quality. We provide services that are superior in nature and make us stand out from the crowd. We offer:
                            </p>
                        </div>
                    </div>
                    <div class="col-md-12 col-md-offset-0 col-sm-10 col-sm-offset-1 col-xs-12 p0 sectionP40">
                        <div class="col-md-6 col-sm-12 col-xs-12">
                            <div data-aos="fade-up" data-aos-duration="1000">
                                <img class="img-responsive centered" src="/assets/front/images/laptop.png"/>
                            </div>
                        </div>
                        <div class="col-md-5 col-sm-12 col-xs-12 sectionP20 pull-right">
                            <div class="acordian gradient-accordian" data-aos="fade-up" data-aos-duration="1000">
                                <div class="col-md-12 col-sm-12 col-xs-12">
                                    <div class="col-md-12 col-sm-12 col-xs-12 pull-right">
                                        <div class="acordian-desc res-txt-center">
                                            <i class="fa fa-pencil"></i><span class="rM">Experienced Writer</span>
                                        </div>
                                    </div>
                                    <div class="col-md-12 col-sm-12 col-xs-12">
                                        <div class="acordian-body res-txt-center">
                                            <span class="white rL">
                                                Not just any writer, but we deploy expert curators on your essay writing projects. Each writer in our pool is qualified, talented and trained in providing specialized niche specific content. With years of experience in the industry, each one of our writers understands the demands of the projects and offer highest quality content accordingly.
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="acordian active gradient-accordian" data-aos="fade-up" data-aos-duration="1000">
                                <div class="col-md-12 col-sm-12 col-xs-12">
                                    <div class="col-md-12 col-sm-12 col-xs-12 pull-right">
                                        <div class="acordian-desc res-txt-center">
                                            <i class="fa fa-paint-brush"></i><span class="rM">Editing and proofreading</span>
                                        </div>
                                    </div>
                                    <div class="col-md-12 col-sm-12 col-xs-12">
                                        <div class="acordian-body res-txt-center">
                                            <span class="white rL">
                                                Enhance the quality of pre-written essays with professional editing and proofreading services. We are language and essay writing experts with hands-on knowledge or different writing styles and grammar. Allow us a chance to beautify your content to the highest quality levels.
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="acordian gradient-accordian" data-aos="fade-up" data-aos-duration="1000">
                                <div class="col-md-12 col-sm-12 col-xs-12">
                                    <div class="col-md-12 col-sm-12 col-xs-12 pull-right">
                                        <div class="acordian-desc res-txt-center">
                                            <i class="fa fa-money"></i><span class="rM">Affordability</span>
                                        </div>
                                    </div>
                                    <div class="col-md-12 col-sm-12 col-xs-12">
                                        <div class="acordian-body res-txt-center">
                                            <span class="white rL">
                                                It takes a lot of efforts to write a perfect piece of an essay and at Essay Royal, we charge you against the hard work. Our services are the most affordable in the industry making us the first choice of people seeking quality and affordable services. For the sake of offering budget-friendly services, we do not compromise with the content quality and deliver the best services only.
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="acordian gradient-accordian" data-aos="fade-up" data-aos-duration="1000">
                                <div class="col-md-12 col-sm-12 col-xs-12">
                                    <div class="col-md-12 col-sm-12 col-xs-12 pull-right">
                                        <div class="acordian-desc res-txt-center">
                                            <i class="fa fa-lock"></i><span class="rM">Privacy</span>
                                        </div>
                                    </div>
                                    <div class="col-md-12 col-sm-12 col-xs-12">
                                        <div class="acordian-body res-txt-center">
                                            <span class="white rL">
                                                Our primary motive is to cater to the students with quality essay writing while maintaining full confidentiality. Each project we undertake is managed with utmost confidentiality. We make sure that your privacy is requested to the best and the credit of the essay goes under your name. This is a business ethics that we follow to allow our customers to enjoy peace of mind while our experts are working on their essay topics.  Your name and personal details along with college/ university details are kept confidential throughout the project.
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- What Can We Offer -->

<!-- Testimonials -->
<section id="testimonial-section" class="hiw-bg">
    <div class="blue-bg sectionP60">
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <div class="col-md-8 col-md-offset-2 col-sm-10 col-sm-offset-1 col-xs-12 text-center">
                        <div  data-aos="fade-up" data-aos-duration="1000">
                            <div class="heading-text">
                                <span class="gold">WHY PEOPLE L<i class="fa fa-heart-o"></i>VE US?</span>
                            </div>
                            <p class="white oR" style="font-size: 16px;">Every review so important for us!</p>
                        </div>
                    </div>
                    <div class="col-md-12 col-sm-12 col-xs-12 sectionP60" style="padding-bottom: 0">
                        <div id="testimonial">
                            <div class="item col-md-12">
                                <div class="testimonial">
                                    <div class="testi-text">
                                        <p class="white rL" >Thanks to Essay Royal Team, for the prepared work for me on time. <br> As always, the work is done perfectly and no edits to do was necessary. I will use your services again.</p>
                                        <span class="gold-gradient-color rM">Alexander</span>
                                        <small class="light2 or">Student of Pusan University, Korea</small>
                                    </div>
                                    <div class="testi-p-image">
                                        <div class="arrow-image"><img src="/assets/front/images/testimonial/bottom-pic.png"></div>
                                        <div class="person-image"><div><img class="img-responsive" src="/assets/front/images/testimonial/client-1.png"></div></div>
                                    </div>
                                </div>
                            </div>
                            <div class="item col-md-12">
                                <div class="testimonial">
                                    <div class="testi-text">
                                        <p class="white rL" >Great job!<br> It was my first time I used them. I needed an article on economy. To be fair, I was worried a little. However, I received a perfect paper even before the deadline! Everything was done according to the guidelines.
</p>
                                        <span class="gold-gradient-color rM">Nataly</span>
                                        <small class="light2 or">Student of Lomonosov Moscow State University</small>
                                    </div>
                                    <div class="testi-p-image">
                                        <div class="arrow-image"><img src="/assets/front/images/testimonial/bottom-pic.png"></div>
                                        <div class="person-image"><div><img class="img-responsive" src="/assets/front/images/testimonial/client-2.png"></div></div>
                                    </div>
                                </div>
                            </div>
                            <div class="item col-md-12">
                                <div class="testimonial">
                                    <div class="testi-text">
                                        <p class="white rL" >On time and high-quality. <br> Thank you for always being on time, doing tasks that I send you. All was done perfectly. <br>I will recommend you to my friends.</p>
                                        <span class="gold-gradient-color rM">Pablo</span>
                                        <small class="light2 or">My Favourite</small>
                                    </div>
                                    <div class="testi-p-image">
                                        <div class="arrow-image"><img src="/assets/front/images/testimonial/bottom-pic.png"></div>
                                        <div class="person-image"><div><img class="img-responsive" src="/assets/front/images/testimonial/client-3.png"></div></div>
                                    </div>
                                </div>
                            </div>
                            <div class="item col-md-12">
                                <div class="testimonial">
                                    <div class="testi-text">
                                        <p class="white rL" >The order was completed on time. I'd like to express my thanks for Essay Royals help. My professor praised me for this work. Once again I express my gratitude to you. Keep up your business! All the best.</p>
                                        <span class="gold-gradient-color rM">Louise Flores</span>
                                        <small class="light2 or">Student of Phoenix University</small>
                                    </div>
                                    <div class="testi-p-image">
                                        <div class="arrow-image"><img src="/assets/front/images/testimonial/bottom-pic.png"></div>
                                        <div class="person-image"><div><img class="img-responsive" src="/assets/front/images/testimonial/client-1.png"></div></div>
                                    </div>
                                </div>
                            </div>
                            <div class="item opacity col-md-12">
                                <div class="testimonial">
                                    <div class="testi-text">
                                        <p class="white rL" >
Thank you a lot. <br> Id never have thought that its possible to write my course work in such a short time. I'll ask for your services in future.</p>
                                        <span class="gold-gradient-color rM">Victor</span>
                                        <small class="light2 or">Student of Seattle University</small>
                                    </div>
                                    <div class="testi-p-image">
                                        <div class="arrow-image"><img src="/assets/front/images/testimonial/bottom-pic.png"></div>
                                        <div class="person-image"><div><img class="img-responsive" src="/assets/front/images/testimonial/client-2.png"></div></div>
                                    </div>
                                </div>
                            </div>
                            <div class="item opacity col-md-12">
                                <div class="testimonial">
                                    <div class="testi-text">
                                        <p class="white rL" >My experience has been first class. Prompt support and feedback from the writer. Was skeptical at first in investing in this type of service however, it has far exceeded my expectations.</p>
                                        <span class="gold-gradient-color rM">James Reed</span>
                                        <small class="light2 or">Student of UTS, Sydney, Australia</small>
                                    </div>
                                    <div class="testi-p-image">
                                        <div class="arrow-image"><img src="/assets/front/images/testimonial/bottom-pic.png"></div>
                                        <div class="person-image"><div><img class="img-responsive" src="/assets/front/images/testimonial/client-3.png"></div></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- Testimonials -->


