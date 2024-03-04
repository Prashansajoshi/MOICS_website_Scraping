import scrapy
from config import categories, pages, offices, treaties

class MOICS(scrapy.Spider):
    name = "moics"
    start_urls = ['https://moics.gov.np/en']
    allowed_domain = ["moics.gov.np/en"]


    def start_requests(self):
       
       # Send a request for the main page
       yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

       # Scrape individual pages within specified categories
       for indv_category in categories:
            yield scrapy.Request(f"https://moics.gov.np/en/category/{indv_category}", callback=self.parse_files, meta={'news_cat': indv_category})

        # Scrape specific pages
       for indv_page in pages:
            yield scrapy.Request(f"https://moics.gov.np/en/pages/{indv_page}", callback=self.parse_files, meta={'indv_page': indv_page})

        # Scrape pages with PNG files
       for indv_office in offices:
            yield scrapy.Request(f"https://moics.gov.np/en/office-link/{indv_office}", callback=self.parse_png_files, meta={'indv_office': indv_office})

        # Scrape International Trade with PDF files
       for indv_treaty in treaties:
            yield scrapy.Request(f"https://moics.gov.np/en/treaty/{indv_treaty}", callback=self.parse_treaty, meta={'indv_treaty': indv_treaty})

       # Send a request for the contact us page
       yield scrapy.Request(url='https://moics.gov.np/en/contact-us', callback=self.parse_contact_us)



    

    def parse_files(self, response):
        # Extract PDF links within the category
            pdf_links = response.css('a[href$=".pdf"]::attr(href)').getall()
            
            for pdf_link in pdf_links:
                  pdf_title = response.css('.tabs-body-content table.table tbody tr td:nth-child(2)::text').get()
                  yield {
                    'category': response.meta['news_cat'],
                    'pdf_link': pdf_link,
                    'pdf_title': pdf_title
                }
                  
        # Extract information from pages that satisfy the URL http://moics.gov.np/en/pages
            if "moics.gov.np/en/pages" in response.url:
                introduction = response.css('.page-detail-content p::text').getall()
                image_link = response.css('.row .col-lg-12 img::attr(src)').getall()

                yield {
                     'pages':response.meta['indv_page'],
                     'introduction': introduction,
                     'image_link': image_link,
                     'url': response.url,
                }


    def parse_png_files(self, response):
        # Extract unique PNG file links along with titles
        png_links = response.css('img[src$=".png"]::attr(src)').getall()
        png_title_elements = response.css('.tabs-body-content table#examplenewmeeraj tbody tr td:nth-child(2) a.text-left')

        for png_link, title_element in zip(png_links, png_title_elements):
            png_title = title_element.css('::text').get()

            yield {
                'office-link': response.meta['indv_office'],
                'png_title': png_title.strip() if png_title else None,
                'png_link': png_link,
                'url': response.url,
            }

    def parse_treaty(self, response):
        # Check if the URL contains "moics.gov.np/en/treaty"
        if "moics.gov.np/en/treaty" in response.url:
            # Extract PDF links within the category
            pdf_links = response.css('a[href$=".pdf"]::attr(href)').getall()

            for pdf_link in pdf_links:
                pdf_title = response.css('.tabs-body-content table.table tbody tr td:nth-child(2)::text').get()
                yield {
                    'treaty': response.meta['indv_treaty'],
                    'pdf_link': pdf_link,
                    'pdf_title': pdf_title
                }

    def parse_contact_us(self, response):
         forms = response.css('.c-from')

         for form in forms:
              title= form.css('ul.list-unstyled li .s-title-section::text').get()
              content= form.css('.i-d-contents .i-d-content::text').get()
              contact = form.css('.i-d-content span a::text').get()
              address = form.css('.i-d-content span:text').get()

              yield{
                "type": "Contact Information",
                "data": {
                   'title': title,
                   'content': content,
                   'contact': contact,
                   'address':address
              }
              }

                  
        
    def parse(self, response):

        #Scraping Front Page
        Notices = response.css(".demo1 ul.list-unstyled li a ::attr(href)").getall()
        pressRelease = response.css("#order ul.list-unstyled li a::attr(href)").getall()
        images = response.css(".carousel-inner .carousel-item img::attr(src)").getall()
        data = response.css(".overflow-auto a::attr(href)").getall()

        yield{
                "Notices": Notices,
                "Press_Release": pressRelease,
                "main_Images" : images,
                "Data" : data
            }
        
        activities = response.css(".overflow-auto .ar-section")

        for activity in activities:
            image = activity.css(".img-section-sno img::attr(src)").getall()
            desc = activity.css("h3.sno-title-text::text").get()
            yield{
                "type": "Ministerial Activities",
                "data": {
                "Images": image,
                "Description" : desc
                }
            }
          




    
        

       


    
