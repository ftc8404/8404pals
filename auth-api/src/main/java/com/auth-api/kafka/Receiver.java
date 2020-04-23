package com.storefront.kafka;

import com.storefront.model.CustomerCases;
import com.storefront.model.CasesStatusChangeEvent;
import com.storefront.respository.CustomerCasesRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.util.concurrent.CountDownLatch;

@Slf4j
@Component
public class Receiver {

    @Autowired
    private CustomerCasesRepository customerCasesRepository;

    @Autowired
    private MongoTemplate mongoTemplate;

    private CountDownLatch latch = new CountDownLatch(1);

    public CountDownLatch getLatch() {

        return latch;
    }

    @KafkaListener(topics = "${spring.kafka.topic.accounts-customer}")
    public void receiveCustomerCases(CustomerCases customerCases) {

        log.info("received payload='{}'", customerCases);
        latch.countDown();
        customerCasesRepository.save(customerCases);
    }

    @KafkaListener(topics = "${spring.kafka.topic.fulfillment-cases}")
    public void receiveCasesStatusChangeEvents(CasesStatusChangeEvent casesStatusChangeEvent) {

        log.info("received payload='{}'", casesStatusChangeEvent);
        latch.countDown();

        Criteria criteria = Criteria.where("cases.guid")
                .is(casesStatusChangeEvent.getGuid());
        Query query = Query.query(criteria);

        Update update = new Update();
        update.addToSet("cases.$.casesStatusEvents", casesStatusChangeEvent.getCasesStatusEvent());
        mongoTemplate.updateFirst(query, update, "customer.cases");
    }
}