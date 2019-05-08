def get_index(): 
    html = '''
 <!-- Post Request! -->
  <form action="/result" method="POST">

    <div class="container">
      <div class="row">
        <div class="col-lg-12 text-center">
          <h2 class="section-heading text-uppercase">Choose Your Favorites</h2>
          <h3 class="section-subheading text-muted">Then, we will recommend to you 10 classic movies you should see!</h3>
        </div>
      </div>
      <div class="row text-center">

        <div class="col-md-3">
          <span class="fa-stack fa-4x">
            <i class="fas fa-circle fa-stack-2x text-primary"></i>
            <i class="fas fa-film fa-stack-1x fa-inverse"></i>
          </span>
          <h4 class="service-heading">Choose Your 1st Movie:</h4>
              
                  <!-- DropDown -->
                  <select name="movie_1">
                      <option value="1">Forrest Gump</option>
                      <option value="2">Mission Impossible</option>
                      <option value="3">101 Dalmations</option>
                      <option value="4">20,000 Leagues Under the Sea</option>
                  </select> 
              
        </div>

        <div class="col-md-3">
            <span class="fa-stack fa-4x">
              <i class="fas fa-circle fa-stack-2x text-primary"></i>
              <i class="fas fa-film fa-stack-1x fa-inverse"></i>
            </span>
            <h4 class="service-heading">Choose Your 2nd Movie:</h4>
                
                    <!-- DropDown -->
                    <select name="movie_2">
                        <option value="1">Forrest Gump</option>
                        <option value="2">Mission Impossible</option>
                        <option value="3">101 Dalmations</option>
                        <option value="4">20,000 Leagues Under the Sea</option>
                    </select> 
                
          </div>

          <div class="col-md-3">
              <span class="fa-stack fa-4x">
                <i class="fas fa-circle fa-stack-2x text-primary"></i>
                <i class="fas fa-film fa-stack-1x fa-inverse"></i>
              </span>
              <h4 class="service-heading">Choose Your 3rd Movie:</h4>
                  
                      <!-- DropDown -->
                      <select name="movie_3">
                          <option value="1">Forrest Gump</option>
                          <option value="2">Mission Impossible</option>
                          <option value="3">101 Dalmations</option>
                          <option value="4">20,000 Leagues Under the Sea</option>
                      </select> 
                  
            </div>

            <div class="col-md-3">
                <span class="fa-stack fa-4x">
                  <i class="fas fa-circle fa-stack-2x text-primary"></i>
                  <i class="fas fa-film fa-stack-1x fa-inverse"></i>
                </span>
                <h4 class="service-heading">Choose Your 4th Movie:</h4>
                    
                        <!-- DropDown -->
                        <select name="movie_4">
                            <option value="1">Forrest Gump</option>
                            <option value="2">Mission Impossible</option>
                            <option value="3">101 Dalmations</option>
                            <option value="4">20,000 Leagues Under the Sea</option>
                        </select> 
                    
              </div>
            
              
            <div class="col-md">
              <br><br><br>
            <input class="btn btn-primary btn-xl text-uppercase js-scroll-trigger" type="submit" value="Submit">
            </form>
          </div>

      </div>
    </div>
'''
    return html


def get_result(features):
    html = f'''
<div class="container">
      <div class="row">
        <div class="col-lg-12 text-center">
          <h2 class="section-heading text-uppercase">Choose Your Favorites</h2>
          <h3 class="section-subheading text-muted">Then, we will recommend to you 10 classic movies you should see!</h3>
        </div>
      </div>
      <div class="row text-center">
        <div class="col-md-4">
          <span class="fa-stack fa-4x">
            <i class="fas fa-circle fa-stack-2x text-primary"></i>
            <i class="fas fa-film fa-stack-1x fa-inverse"></i>
          </span>
          <h4 class="service-heading">You Chose: { features }</h4>
          <a class="btn btn-primary btn-xl text-uppercase js-scroll-trigger" href="/index.html#services">Try Again</a>
        </div>
      </div>
    </div>
'''
    return html