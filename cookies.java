// package com.mkyong.csv;
import org.springframework.*;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class Cookies {
             @GetMapping("/")
        public String readCookie(@CookieValue(value = "email", defaultValue = "Atta") String email) {
            // return "Hi! My email is " + email;
            return email;
        }


        @GetMapping("/change-username")
        public String setCookie(HttpServletResponse response) {
            // create a cookie
            Cookie cookie = new Cookie("email", "niemiryan@gmail.com");
            //add cookie to response
            response.addCookie(cookie);
            return "Email is changed!";
        }

        @GetMapping("/all-cookies")
        public String readAllCookies(HttpServletRequest request) {
            Cookie[] cookies = request.getCookies();
            if (cookies != null) {
                return Arrays.stream(cookies)
                        .map(c -> c.getName() + "=" + c.getValue()).collect(Collectors.joining(", "));
            }
            return "No cookies";
        }

    public static void main(String[] args) {
        // create a cookie
        Cookie cookie = new Cookie("email", readCookie().toString());
        cookie.setMaxAge(7 * 24 * 60 * 60); // expires in 7 days
        //add cookie to response
        response.addCookie(cookie);


        //delete cookie by setting the max-age to 0
        // create a cookie
        Cookie cookie = new Cookie("email", null);
        cookie.setMaxAge(0);
        cookie.setSecure(true);
        cookie.setHttpOnly(true);
        cookie.setPath("/");
        //add cookie to response
        response.addCookie(cookie);

        String csvFile = "./email.csv";
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";

        try {

            br = new BufferedReader(new FileReader(csvFile));
            while ((line = br.readLine()) != null) {

                // use comma as separator
                String[] country = line.split(cvsSplitBy);

                for(int i = 0; i < email.length; i++ ) {
                    System.out.println("Email [email= " + email[i]"");
                    if(getCookies().toString().equals(email[i])) {
                        System.out.println("You are ready to go member!")
                    }

                }
            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }    
}


// public class CookieDecoder {

//     private static final Log log = LogFactory.getLog(CookieDecoder.class);

//     /**
//      * @param cookieValue The value of the cookie to decode
//      * @return Returns the decoded string
//      */
//     public String decode(String cookieValue) {
//         if (cookieValue == null || "".equals(cookieValue)) {
//             return null;
//         }
//         if (log.isDebugEnabled()) {
//             log.debug("Decoding string: " + cookieValue);
//         }
//         URLCodec urlCodec = new URLCodec();
//         String b64Str;
//         try {
//             b64Str = urlCodec.decode(cookieValue);
//         }
//         catch (DecoderException e) {
//             log.error("Error decoding string: " + cookieValue);
//             return null;
//         }
//         Base64 base64 = new Base64();
//         byte[] encodedBytes = b64Str.getBytes();
//         byte[] decodedBytes = base64.decode(encodedBytes);
//         String result = new String(decodedBytes);
//         if (log.isDebugEnabled()) {
//             log.debug("Decoded string to: " + result);
//         }
//         return result;
//     }
// }