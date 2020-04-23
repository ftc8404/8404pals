package com.storefront.controller;

import com.storefront.kafka.Sender;
import com.storefront.model.*;
import com.storefront.respository.PALSUsersRepository;
import com.storefront.utilities.SampleData;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import java.sql.Timestamp;
import java.util.Collections;
import java.util.List;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/users")
public class PALSUsersController {

    private PALSUsersRepository palsUsersRepository;

    private MongoTemplate mongoTemplate;

    @Value("${spring.kafka.topic.users-users}") //same thing as users-get
    private String topic;

    private Sender sender;


    @Autowired
    public PALSUsersController(PALSUsersRepository palsUsersRepository,
                                    MongoTemplate mongoTemplate,
                                    Sender sender) {

        this.palsUsersRepository = palsUsersRepository;
        this.mongoTemplate = mongoTemplate;
        this.sender = sender;
    }

    @RequestMapping(path = "/sample/cases", method = RequestMethod.GET)
    public ResponseEntity<String> sampleUsers() {

        List<PALSUsers> palsUsersList = palsUsersRepository.findAll();

        for (PALSUsers palsUsers : palsUsersList) {
            palsUsers.setUsers(SampleData.createSampleUsersHistory());
        }

        palsUsersRepository.saveAll(palsUsersList);

        return new ResponseEntity("Sample cases added to pals cases", HttpStatus.OK);
    }

    @RequestMapping(path = "/summary", method = RequestMethod.GET)
    @ResponseBody
    public ResponseEntity<Map<String, List<PALSUsers>>> palsSummary() {

        List<PALSUsers> palsUsersList = palsUsersRepository.findAll();
        return new ResponseEntity<>(Collections.singletonMap("palss", palsUsersList), HttpStatus.OK);
    }

    @RequestMapping(path = "/sample/fulfill", method = RequestMethod.GET)
    public ResponseEntity<String> fulfillSampleUsers() {

        Criteria elementMatchCriteria = Criteria.where("cases.casesStatusEvents")
                .size(2)
                .elemMatch(Criteria.where("casesStatusType").is(UsersStatusType.CREATED))
                .elemMatch(Criteria.where("casesStatusType").is(UsersStatusType.APPROVED));
        Query query = Query.query(elementMatchCriteria);
        List<PALSUsers> palsUsersList = mongoTemplate.find(query, PALSUsers.class);

        log.info("palsUsersList size: " + palsUsersList.size() + '\n');


        for (PALSUsers palsUsers : palsUsersList) {
            FulfillmentRequestEvent fulfillmentRequestEvent = new FulfillmentRequestEvent();
            Timestamp timestamp = new Timestamp(System.currentTimeMillis());
            fulfillmentRequestEvent.setTimestamp(timestamp.getTime());
            fulfillmentRequestEvent.setName(palsUsers.getName());
            fulfillmentRequestEvent.setContact(palsUsers.getContact());

            Address shippingAddress = palsUsers.getAddresses()
                    .stream()
                    .filter(o -> o.getType().equals(AddressType.SHIPPING))
                    .findFirst()
                    .orElse(null);

            fulfillmentRequestEvent.setAddress(shippingAddress);

            try {
                // cases where the first cases status event in list is created...
                // cases where the last cases status event in list is approved...

                Users pendingUsers = palsUsers.getUsers()
                        .stream()
                        .filter(o -> o.getUsersStatusEvents()
                                .get(0)
                                .getUsersStatusType().equals(UsersStatusType.CREATED))
                        .filter(o -> o.getUsersStatusEvents()
                                .get(o.getUsersStatusEvents().size() - 1)
                                .getUsersStatusType().equals(UsersStatusType.APPROVED))
                        .findFirst()
                        .orElse(null);

                log.info("pending cases: " + pendingUsers);

                fulfillmentRequestEvent.setUsers(pendingUsers);

                sender.send(topic, fulfillmentRequestEvent);

            } catch (NullPointerException ex) {
                log.info(ex.getMessage());
                return new ResponseEntity("No 'Approved' cases found", HttpStatus.NOT_FOUND);
            }

        }
        return new ResponseEntity("All 'Approved' cases sent for fulfillment", HttpStatus.OK);
    }
}
